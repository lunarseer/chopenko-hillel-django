from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.contrib import messages
from django.views.generic import TemplateView, ListView, View

from .forms import SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignupForm()
    return render(request, 'signup_user.html', {'form': form})