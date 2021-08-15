from django.urls import path

from .views import add_group, get_groups, get_groups_list

urlpatterns = [
    path('groups_list/', get_groups_list, name='groups-list'),
    path('add_group/', add_group, name='add-group'),
    path('groups/', get_groups),
]