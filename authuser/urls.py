from django.urls import path

from .views import (
                    login_view,
                    signup_view
)


urlpatterns = [
    path('login_user/', login_view, name='user-login'),
    path('signup_user/', signup_view, name='user-signup')
]
