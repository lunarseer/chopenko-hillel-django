from django.urls import path
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetCompleteView,
                                       PasswordResetDoneView,
                                       )

from .views import (
                    login_view,
                    signup_view,
                    current_user_view,
                    change_password_view,
                    reset_password_view,
                    logout_view
)


urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('current/', current_user_view, name='current-user'),
    path('password_change/', change_password_view, name='password_change'),
    path('password_reset/', reset_password_view, name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', logout_view, name='logout')
]
