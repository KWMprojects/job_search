from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class SavedJobsList(models.Model):
    title = models.CharField(max_length= 50)
    description = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    job_title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    salary_or_hourly = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=25)
    state = models.CharField(max_length=20)
    city_or_town = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)
    added_date = models.DateField(auto_now=True)
    list_item = models.ForeignKey(SavedJobsList, null=True, on_delete=models.SET_NULL)
    added_to_jobs_list = models.BooleanField(default=False)
    
    def __str__(self):
        return self.job_title

class ListPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    savedjoblist = models.ForeignKey(SavedJobsList, on_delete=models.CASCADE)
    is_owner = models.BooleanField(blank=False, default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'savedjoblist'], name='unique_owner'),
        ]

    def __str__(self):
        if self.is_owner:
            fmt = '{} ({}) can write to {} ({})'
        else:
            fmt = '{} ({}) cannot write to {}'
        return fmt.format(self.user.username, self.user.id, self.package.name, self.package.id)

    @classmethod
    def can_write(cls, user, savedjoblist):
        try:
            permission = cls.objects.get(user=user, savedjoblist=savedjoblist)
            return permission.is_owner
        except ObjectDoesNotExist:
            return False

    @classmethod
    def set_can_write(cls, user, savedjoblist):
        obj, created = cls.objects.get_or_create(user=user, savedjoblist=savedjoblist, defaults={'is_owner': True})
        if not created:
            obj.is_owner = True
            obj.save()