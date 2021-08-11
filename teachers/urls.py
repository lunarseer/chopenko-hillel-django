from django.urls import path

from .views import add_teacher, get_teachers

urlpatterns = [
    path('add_teacher', add_teacher),
    path('teachers', get_teachers),
]
