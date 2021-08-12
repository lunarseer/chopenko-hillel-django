from django.urls import path

from .views import (index,
                    generate_student,
                    generate_students,
                    generate_teachers,
                    generate_groups)

urlpatterns = [
    path('', index),
    path('generate_student/', generate_student),
    path('generate_students/', generate_students),
    path('generate_teachers/', generate_teachers),
    path('generate_groups/', generate_groups),
]
