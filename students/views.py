from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Student
from .forms import AddStudentForm, StudentFormFromModel


# Create your views here.


def students_list(request):
    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})


def get_student(request, student_id):
    student = Student.objects.get(id=student_id)
    return HttpResponse(status=200, content=student)


def edit_student(request, student_id):

    def render_edit_form(form):
        return render(request,
                      'edit_student_form.html',
                      {'form': form, 'student_id': student_id})

    if request.method == "POST":
        form = StudentFormFromModel(request.POST)
        if form.is_valid():
            Student.objects.update_or_create(
                                             defaults=form.cleaned_data,
                                             id=student_id)

            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            name = f'{firstname} {lastname}'

            messages.success(request, f'Student {name} saved')
            return redirect('students-list')
        else:
            return render_edit_form(form)

    else:
        student = Student.objects.get(id=student_id)
        form = StudentFormFromModel(instance=student)
        return render_edit_form(form)


def add_student(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            student = Student.objects.create(**formdata)
            name = f'{student.firstname} {student.lastname}'

            messages.success(request, f'Student {name} Added')
            return redirect('students-list')
    else:
        form = AddStudentForm()
    return render(request, 'add_student_form.html', {'form': form})


def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    name = f'{student.firstname} {student.lastname}'
    student.delete()
    messages.success(request, f'Student {name} Deleted')
    return redirect('students-list')
