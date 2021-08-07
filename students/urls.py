from django.urls import path

from . import views as stud

urlpatterns = [
    path('', stud.index),
    path('add_student', stud.add_student),
    path('add_teacher', stud.add_teacher),
    path('add_group', stud.add_group),
    path('generate_student', stud.generate_student),
    path('generate_students', stud.generate_students),
    path('generate_teachers', stud.generate_teachers),
    path('generate_groups', stud.generate_groups),
    path('students', stud.get_students),
    path('groups', stud.get_groups),
    path('teachers', stud.get_teachers),
]
