from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


from .models import Student

from .forms import AddStudentForm


# Create your views here.


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


def get_students(request):
    students = [x.values() for x in Student.objects.all()]
    return JsonResponse(status=200, data=students, safe=False)


