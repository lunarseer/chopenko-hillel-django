from django.urls import path

from .views import (
                    teachers_list,
                    add_teacher,
                    get_teacher,
                    edit_teacher,
                    delete_teacher
                    )

urlpatterns = [
    path('teachers_list/', teachers_list, name='teachers-list'),
    path('add_teacher/', add_teacher, name='add-teacher'),
    path('get_teacher/<int:teacher_id>', get_teacher, name='get-teacher'),
    path('edit_teacher/<int:teacher_id>', edit_teacher, name='edit-teacher'),
    path('delete_teacher/<int:teacher_id>', delete_teacher, name='delete-teacher'),
]
