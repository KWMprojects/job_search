from django.urls import path, include
from .views import SavedJobsListView, current_user, UserList
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Saved_Job_List', SavedJobsListView)

urlpatterns = [
    path('', include(router.urls)),
    path('current_user/', current_user),
    path('users/', UserList.as_view())
]