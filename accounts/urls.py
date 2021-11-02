from django.urls import path

from .views import (
                    login_view,
                    signup_view,
                    current_user_view,
                    change_password_view,
                    reset_password_view,
                    reset_password_done_view,
                    logout_view
)


urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('current/', current_user_view, name='current-user'),
    path('change_password/', change_password_view, name='change-password'),
    path('reset_password/', reset_password_view, name='reset-password'),
    path('reset_password_done/', reset_password_done_view, name='reset-password-done'),
    path('logout/', logout_view, name='logout')
]
