import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from faker import Faker

from .models import (Group,
                     Student,
                     Teacher)

from .forms import (AddStudentForm,
                    AddTeacherForm,
                    AddGroupForm,
                    GeneratorCountForm)


# Create your views here.

def index(request):
    return render(request, 'index.html')


def add_student(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            person = Student.objects.create(firstname=formdata['firstname'],
                                            lastname=formdata['lastname'],
                                            age=formdata['age'])
            entitylist = [f"{person.firstname} {person.lastname}"]
            data = {'message': '1 student created', 'entitylist': entitylist}
            return render(request, 'entity_responce.html', data)
    else:
        form = AddStudentForm()
    return render(request, 'add_student_form.html', {'form': form})


def add_teacher(request):
    if request.method == "POST":
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            person = Teacher.objects.create(firstname=formdata['firstname'],
                                            lastname=formdata['lastname'],
                                            age=formdata['age'])
            entitylist = [f"{person.firstname} {person.lastname}"]
            data = {'message': '1 teacher created', 'entitylist': entitylist}
            return render(request, 'entity_responce.html', data)
    else:
        form = AddStudentForm()
    return render(request, 'add_teacher_form.html', {'form': form})


def add_group(request):
    if not all([Student.objects.all(), Teacher.objects.all()]):
        return HttpResponse("Add Students and Teachers first")
    if request.method == "POST":
        form = AddGroupForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            group = Group.objects.create(name=formdata['name'],
                                         discipline=formdata['discipline'])
            data = {'message': '1 groups created', 'entitylist': [group.name]}
            return render(request,
                          'entity_responce.html',
                          data)
        else:
            return HttpResponse('Invalid Form', form.fields)
    else:
        form = AddGroupForm()
    return render(request, 'add_group_form.html', {'form': form})


def get_students(request):
    students = [x.values() for x in Student.objects.all()]
    return JsonResponse(status=200, data=students, safe=False)


def get_groups(request):
    response = [x.values() for x in Group.objects.all()]
    return JsonResponse(status=200, data=response, safe=False)


def get_teachers(request):
    query = {q: v for q, v in request.GET.items()}
    try:
        response = [x.values() for x in Teacher.objects.filter(**query)]
    except Exception as e:
        return JsonResponse(status=404, data={"message": str(e)})
    return JsonResponse(status=200, data=response, safe=False)


# DEPRECATED
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
