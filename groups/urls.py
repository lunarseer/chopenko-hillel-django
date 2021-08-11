from django.urls import path

from .views import add_group, get_groups

urlpatterns = [
    path('add_group', add_group),
    path('groups', get_groups),
]