import random
from faker import Faker

from django.shortcuts import render, redirect
from django.contrib import messages

from students.models import Student
from teachers.models import Teacher
from groups.models import Group

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
            students = []
            count = form.cleaned_data.get('count')
            gen = Faker()
            for _ in range(count):
                stud = Student(firstname=gen.first_name(),
                               lastname=gen.last_name(),
                               age=random.randint(16, 52))
                students.append(stud)
            Student.objects.bulk_create(students)
            messages.success(request, f'{len(students)} Students Generated.')
            return redirect('students-list')
    elif request.method == "GET":
        form = GeneratorCountForm()
        return render(request, 'generate_form.html',
                      {'form': form, 'entitytype': 'students'})


def generate_teachers(request):
    if request.method == "POST":
        form = GeneratorCountForm(request.POST)
        if form.is_valid():
            teachers = []
            count = form.cleaned_data.get('count')
            gen = Faker()
            for _ in range(count):
                teacher = Teacher(firstname=gen.first_name(),
                                  lastname=gen.last_name(),
                                  age=random.randint(16, 52))
                teachers.append(teacher)
            Teacher.objects.bulk_create(teachers)
            messages.success(request, f'{len(teachers)} Teachers Generated.')
            return redirect('teachers-list')
    elif request.method == "GET":
        form = GeneratorCountForm()
        return render(request, 'generate_form.html',
                      {'form': form, 'entitytype': 'teachers'})


def generate_groups(request):
    if request.method == "POST":
        form = GeneratorCountForm(request.POST)
        if form.is_valid():
            teachers = Teacher.objects.all()
            students = Student.objects.all()
            num_teachers = len(teachers)
            num_students = len(students)
            count = form.cleaned_data.get('count')
            groups = []
            for _ in range(count):
                teacher = teachers[int(random.randrange(0, num_teachers))]
                headman = students[int(random.randrange(0, num_students))]
                print(teacher, headman)
                group = Group(name=f'{teacher.firstname}_group', teacher=teacher, headman=headman)
                groups.append(group)
            Group.objects.bulk_create(groups)
            messages.success(request, f'{len(groups)} Groups Generated.')
            return redirect('groups-list')
    elif request.method == "GET":
        form = GeneratorCountForm()
        return render(request, 'generate_form.html',
                      {'form': form, 'entitytype': 'groups'})
