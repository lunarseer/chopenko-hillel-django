from django.urls import path

from .views import (IndexView,
                    CurrencyView,
                    ContactUsView,
                    FakeGeneratorView,
                    StudentsGeneratorView,
                    TeachersGeneratorView,
                    GroupsGeneratorView)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('fake_generator/',
         FakeGeneratorView.as_view(),
         name='fake-generator'),
    path('contact_us/',
         ContactUsView.as_view(),
         name='contact-us'),
    path('currencies/',
         CurrencyView.as_view(),
         name='currencies-list'),
    path('generate_students/',
         StudentsGeneratorView.as_view(),
         name='generate-students'),
    path('generate_teachers/',
         TeachersGeneratorView.as_view(),
         name='generate-teachers'),
    path('generate_groups/',
         GroupsGeneratorView.as_view(),
         name='generate-groups'),
]
