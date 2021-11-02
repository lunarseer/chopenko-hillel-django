from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, View
from django.template.defaultfilters import striptags

from .forms import SignupForm, LoginForm, ChangePasswordForm, ResetPasswordForm
import pdb


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
    return render(request, 'change_password.html', {'form': form})


def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            return redirect('reset-password-done')
    else:            
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})


def reset_password_done_view(request):
    return render(request, 'reset_password_done.html', {})


def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user
            messages.add_message(request, messages.SUCCESS, f'Good Bye, {username}!')
            logout(request)
            return redirect('home')
