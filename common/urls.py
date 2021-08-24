from django.urls import path

from .views import (index,
                    fake_generator_page,
                    generate_students,
                    generate_teachers,
                    generate_groups)

urlpatterns = [
    path('', index, name='home'),
    path('fake_generator/', fake_generator_page, name='fake-generator'),
    path('generate_students/', generate_students, name='generate-students'),
    path('generate_teachers/', generate_teachers, name='generate-teachers'),
    path('generate_groups/', generate_groups, name='generate-groups'),
]
