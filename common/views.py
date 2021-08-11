import random
from faker import Faker

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from students.models import Student
from teachers.models import Teacher
from groups.models import Group

from .forms import GeneratorCountForm


def index(request):
    return render(request, 'index.html')

def generate_student(request):
    gen = Faker()
    stud = Student.objects.create(firstname=gen.first_name(),
                                  lastname=gen.last_name(),
                                  age=random.randint(16, 52))
    return JsonResponse(status=200, data=[stud.values()], safe=False)


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
            entitylist = [f'{x.firstname} {x.lastname}' for x in students]
            data = {'message': f'{count} students created',
                    'entitylist': entitylist}
            return render(request, 'entity_responce.html', data)
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
            entitylist = [f'{x.firstname} {x.lastname}' for x in teachers]
            data = {'message': f'{count} students created',
                    'entitylist': entitylist}
            return render(request, 'entity_responce.html', data)
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
            data = {'message': f'{count} groups created',
                    'entitylist': [f'{x.name}' for x in groups]}
            return render(request, 'entity_responce.html', data)
    elif request.method == "GET":
        form = GeneratorCountForm()
        return render(request, 'generate_form.html',
                      {'form': form, 'entitytype': 'groups'})
