from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.contrib import messages
from django.views.generic import TemplateView, ListView, View
from django.template.defaultfilters import striptags

from .forms import SignupForm, LoginForm
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
                print(user)
                login(request, user)
            else:
                messages.error(request, f'User {username} not authorized')
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
            # login(request, user)
            return redirect('home')
        else:
            errors = dict(form.errors)
            for field, error in errors.items():
                messages.error(request, f'{field}:{striptags(error)}')
    else:
        form = SignupForm()
    return render(request, 'signup_user.html', {'form': form})

def current_user_view(request):
    return render(request, 'current_user.html', {})


def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('home')
