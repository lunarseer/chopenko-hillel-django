from django.urls import path

from .views import (index,
                    get_currencies,
                    contact_us,
                    fake_generator_page,
                    generate_students,
                    generate_teachers,
                    generate_groups)

urlpatterns = [
    path('', index, name='home'),
    path('fake_generator/', fake_generator_page, name='fake-generator'),
    path('contact_us/', contact_us, name='contact-us'),
    path('currencies/', get_currencies, name='currencies-list'),
    path('generate_students/', generate_students, name='generate-students'),
    path('generate_teachers/', generate_teachers, name='generate-teachers'),
    path('generate_groups/', generate_groups, name='generate-groups'),
]
