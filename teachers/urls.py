from django.urls import path

from .views import (
                    TeachersListView,
                    TeacherAddView,
                    TeacherEditView,
                    TeacherDeleteView
                    )

urlpatterns = [
    path('teachers_list/',
         TeachersListView.as_view(),
         name='teachers-list'),
    path('add_teacher/',
         TeacherAddView.as_view(),
         name='add-teacher'),
    path('edit_teacher/<int:id>',
         TeacherEditView.as_view(),
         name='edit-teacher'),
    path('delete_teacher/<int:id>',
         TeacherDeleteView.as_view(),
         name='delete-teacher'),
]
