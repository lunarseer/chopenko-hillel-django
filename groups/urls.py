from django.urls import path


from .views import (
                    GroupsListView,
                    GroupAddView,
                    GroupEditView,
                    GroupDeleteView
                    )


urlpatterns = [
    path('groups_list/', GroupsListView.as_view(), name='groups-list'),
    path('add_group/', GroupAddView.as_view(), name='add-group'),
    path('edit_group/<int:id>', GroupEditView.as_view(), name='edit-group'),
    path('delete_group/<int:id>', GroupDeleteView.as_view(), name='delete-group'),
]
