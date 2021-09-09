from django.core.management import call_command

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import GeneratorCountForm, ContactForm
from .tasks import send_mail_message


def index(request):
    return render(request, 'index.html')


def fake_generator_page(request):
    return render(request, 'fake_generator.html', {})


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_to = [
                'lunarseer.test@gmail.com',
                ]
            subject = form.cleaned_data.get('subject')
            send_from = form.cleaned_data.get('send_from')
            message = form.cleaned_data.get('message')
            send_mail_message.delay(send_to=send_to,
                                    subject=subject,
                                    send_from=send_from,
                                    message=message)
            messages.success(request, 'Email Sent.')
            return redirect('home')
    elif request.method == "GET":
        form = ContactForm()
        return render(request, 'contact_us.html',
                      {'form': form, 'entitytype': 'students'})


def generate_students(request):
    if request.method == "POST":
        form = GeneratorCountForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data.get('count')
            call_command('generate_students', count=count)
            messages.success(request, f'{count} Students Generated.')
            return redirect('students-list')
    elif request.method == "GET":
        form = GeneratorCountForm()
        return render(request, 'generate_form.html',
                      {'form': form, 'entitytype': 'students'})


def generate_teachers(request):
    if request.method == "POST":
        form = GeneratorCountForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data.get('count')
            call_command('generate_teachers', count=count)
            messages.success(request,
                             f'{count} Teachers and Groups Generated.')
            return redirect('teachers-list')
    elif request.method == "GET":
        form = GeneratorCountForm()
        return render(request, 'generate_form.html',
                      {'form': form, 'entitytype': 'teachers'})


def generate_groups(request):
    if request.method == "POST":
        form = GeneratorCountForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data.get('count')
            call_command('generate_groups', count=count)
            messages.success(request, f'{count} Groups Generated.')
            return redirect('groups-list')
    elif request.method == "GET":
        form = GeneratorCountForm()
        return render(request, 'generate_form.html',
                      {'form': form, 'entitytype': 'groups'})
