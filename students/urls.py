from django.urls import path

from .views import (
                    add_student,
                    get_student,
                    students_list,
                    edit_student,
                    delete_student
)


urlpatterns = [
    path('students_list/', students_list, name='students-list'),
    path('add_student/', add_student, name='add-student'),
    path('get_student/<int:student_id>', get_student, name='get-student'),
    path('edit_student/<int:student_id>', edit_student, name='edit-student'),
    path('delete_student/<int:student_id>',
         delete_student,
         name='delete-student'),
]
