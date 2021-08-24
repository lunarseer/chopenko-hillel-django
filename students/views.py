from django.http import HttpResponse
from django.shortcuts import render, redirect

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
    if request.method == "POST":
        form = StudentFormFromModel(request.POST)
        if form.is_valid():
            Student.objects.update_or_create(
                                             defaults=form.cleaned_data,
                                             id=student_id)
            return redirect('students-list')
    else:
        student = Student.objects.get(id=student_id)
        form = StudentFormFromModel(instance=student)
        return render(
                      request,
                      'edit_student_form.html',
                      {'form': form, 'student_id': student_id})


def add_student(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            Student.objects.create(firstname=formdata['firstname'],
                                   lastname=formdata['lastname'],
                                   age=formdata['age'])
            return redirect('students-list')
    else:
        form = AddStudentForm()
    return render(request, 'add_student_form.html', {'form': form})


def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.delete()
    return redirect('students-list')
