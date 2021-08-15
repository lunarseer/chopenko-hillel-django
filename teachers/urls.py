from django.urls import path

from .views import add_teacher, get_teachers, get_teachers_list

urlpatterns = [
    path('teachers_list/', get_teachers_list, name='teachers-list'),
    path('add_teacher/', add_teacher, name='add-teacher'),
    path('teachers/', get_teachers),
]
