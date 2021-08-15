from django.urls import path


from .views import (
                    groups_list,
                    add_group,
                    get_group,
                    edit_group,
                    delete_group
                    )


urlpatterns = [
    path('groups_list/', groups_list, name='groups-list'),
    path('add_group/', add_group, name='add-group'),
    path('get_group/<int:group_id>', get_group, name='get-group'),
    path('edit_group/<int:group_id>', edit_group, name='edit-group'),
    path('delete_group/<int:group_id>', delete_group, name='delete-group'),
]