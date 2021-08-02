import random

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from faker import Faker

from .models import Group, Student, Teacher


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


def generate_student(request):
    gen = Faker()
    stud = Student.objects.create(firstname=gen.first_name(),
                                  lastname=gen.last_name(),
                                  age=random.randint(16, 52))
    return JsonResponse(status=200, data=[stud.values()], safe=False)


@csrf_exempt    # CSRF TOKEN DECORATOR, I DUNNO BUT IT HELPS
def generate_students(request):
    gen = Faker()
    if request.method != "POST":
        responce = "{} method not implemented".format(request.method)
    if request.method == "POST":
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


@csrf_exempt
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


@csrf_exempt
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
