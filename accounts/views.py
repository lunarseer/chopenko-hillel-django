from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .forms import SignupForm, LoginForm, ChangePasswordForm, ResetPasswordForm
from common.tasks import send_mail_message

from os import getenv


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username')
            raw_password = cd.get('password')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                messages.add_message(request, messages.INFO, f'Welcome back, {username}!')
            else:
                messages.add_message(request, messages.WARNING, f'Wrong username or password!')
                return render(request, 'login_user.html', {'form': form})
            return redirect('home')

    else:
        form = LoginForm()
    return render(request, 'login_user.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                return redirect('home')
        else:
            errors = dict(form.errors)
            for field, error in errors.items():
                messages.add_message(request, messages.ERROR, f'{field}:{striptags(error)}')
    else:
        form = SignupForm()
    return render(request, 'signup_user.html', {'form': form})


def current_user_view(request):
    if request.user.is_authenticated:
        return render(request, 'current_user.html', {})
    return redirect('home')


def change_password_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            raw_password = cd.get('password1','')
            user = User.objects.get(username__exact=request.user)
            user.set_password(raw_password)
            user.save()
            messages.add_message(request, messages.INFO, f'Log in back with a new password, {user.username}!')
            logout(request)
            return redirect('home')
    else:
        form = ChangePasswordForm()
    return render(request, 'password_change.html', {'form': form})


def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data.get('email')
            users = User.objects.filter(email=value)
            if users.exists():
                for user in users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    send_from = getenv('EMAIL_HOST_USER')
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
					}
                    message = render_to_string(email_template_name, c)
                    try:
                        send_mail_message.delay(send_to=[user.email],
                                                subject=subject,
                                                send_from=send_from,
                                                message=message)
                        messages.success(request, 'Email Sent.')
                    except Exception as e:
                        messages.error(request, f'Email Not Sent! Celery Message: {e}')
            return redirect('password_reset_done')
    else:            
        form = ResetPasswordForm()
    return render(request, 'password_reset.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user
            messages.add_message(request, messages.SUCCESS, f'Good Bye, {username}!')
            logout(request)
            return redirect('home')
