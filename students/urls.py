from django.urls import path

from .views import (
                    StudentAddView,
                    StudentsList,
                    StudentEditView,
                    StudentDeleteView
)


urlpatterns = [
    path('students_list/', StudentsList.as_view(), name='students-list'),
    path('add_student/', StudentAddView.as_view(), name='add-student'),
    path('edit_student/<int:id>',
         StudentEditView.as_view(),
         name='edit-student'),
    path('delete_student/<int:id>',
         StudentDeleteView.as_view(),
         name='delete-student'),
]
