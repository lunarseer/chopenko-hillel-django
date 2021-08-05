import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from faker import Faker

from .models import Group, Student, Teacher
from .forms import AddStudentForm, AddTeacherForm, AddGroupForm


def validate_count(count):
    if isinstance(count, str):
        try:
            return int(count)
        except ValueError:
            return 0
    if isinstance(count, int):
        return count
    if isinstance(count, float):
        return int(count)


# Create your views here.

def index(request):
    return render(request, 'index.html')


def add_student(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            person = Student.objects.create(firstname=request.POST.get('firstname'),
                                lastname=request.POST.get('lastname'),
                                age=request.POST.get('age'))
            return render(request, 'entity_responce.html', {'entity': person, 'oname':person.itemname()})
    else:
        form = AddStudentForm()
    return render(request, 'add_student_form.html', {'form': form})

def add_teacher(request):
    if request.method == "POST":
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            person = Teacher.objects.create(firstname=request.POST.get('firstname'),
                                lastname=request.POST.get('lastname'),
                                age=request.POST.get('age'))
            return render(request, 'entity_responce.html', {'entity': person, 'oname':person.itemname()})
    else:
        form = AddStudentForm()
    return render(request, 'add_teacher_form.html', {'form': form})


def add_group(request):
    if not all([Student.objects.all(), Teacher.objects.all()]):
        return HttpResponse("Add Students and Teachers first")
    if request.method == "POST":
        print(str(request.POST.get('teachers')))
        form = AddGroupForm(
            name=request.POST.get('name'),
            students=[x for x in request.POST.get('students').items()],
            teachers=request.POST.get('teachers'),
            )
        print(form.fields)
        if form.is_valid():
            group = Group.objects.create(name=request.POST.get('name'),
                                students=request.POST.get('students'),
                                teachers=request.POST.get('teachers'))
            return render(request, 'entity_responce.html', {'entity': group, 'oname':group.itemname()})
        else:
            return HttpResponse('Invalid Form', form.fields)
    else:
        teachers = [(x.id, str(x)) for x in Teacher.objects.all()]
        students = [(x.id, str(x)) for x in Student.objects.all()]
        form = AddGroupForm(students=students, teachers=teachers)
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


#DEPRECATED
def generate_student(request):
    gen = Faker()
    stud = Student.objects.create(firstname=gen.first_name(),
                                  lastname=gen.last_name(),
                                  age=random.randint(16, 52))
    return JsonResponse(status=200, data=[stud.values()], safe=False)


#DEPRECATED
def generate_students(request):
    gen = Faker()
    if request.method != "POST":
        responce = "{} method not implemented".format(request.method)
    else:
        count = validate_count(request.POST.get('count', 0))
        if count > 0:
            students = []
            for _ in range(count):
                stud = Student.objects.create(firstname=gen.first_name(),
                                              lastname=gen.last_name(),
                                              age=random.randint(16, 52))
                students.append(stud)
            responce = [x.values() for x in students]
        else:
            return JsonResponse(status=500,
                                data={"status": "error",
                                      "message": "Wrong Count Value"})
    return JsonResponse(status=200, data=responce, safe=False)


#DEPRECATED
def generate_teachers(request):
    gen = Faker()
    if request.method != "POST":
        responce = "{} method not implemented".format(request.method)
    if request.method == "POST":
        count = validate_count(request.POST.get('count', 0))
        if count > 0:
            teachers = []
            for _ in range(count):
                teacher = Teacher.objects.create(firstname=gen.first_name(),
                                                 lastname=gen.last_name(),
                                                 age=random.randint(16, 52))
                teachers.append(teacher)
            responce = [x.values() for x in teachers]
        else:
            return HttpResponse("Wrong Count Value")
    return HttpResponse(responce)


#DEPRECATED
def generate_groups(request):
    if request.method != "POST":
        responce = "{} method not implemented".format(request.method)
    if request.method == "POST":
        count = validate_count(request.POST.get('count', 0))
        if count > 0:
            groups = []
            for i in range(count):
                group = Group.objects.create(name=f"group_{i}")
                groups.append(group)
            responce = [x.values() for x in groups]
        else:
            return HttpResponse("Wrong Count Value")
    return HttpResponse(responce)
