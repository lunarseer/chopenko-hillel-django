import random
from faker import Faker

from django.shortcuts import render, redirect

from students.models import Student
from teachers.models import Teacher
from groups.models import Group

from .forms import GeneratorCountForm


def index(request):
    return render(request, 'index.html')


def fake_generator_page(request):
    return render(request, 'fake_generator.html', {})


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
            num_teachers = len(teachers)
            count = form.cleaned_data.get('count')
            groups = []
            for _ in range(count):
                teacher = teachers[int(random.randrange(0, num_teachers))]
                group = Group(name=f'{teacher.firstname}_group')
                groups.append(group)
            Group.objects.bulk_create(groups)
            return redirect('groups-list')
    elif request.method == "GET":
        form = GeneratorCountForm()
        return render(request, 'generate_form.html',
                      {'form': form, 'entitytype': 'groups'})
