from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Student
from .forms import AddStudentForm, StudentFormFromModel
from common.forms import ConfirmActionForm


# Create your views here.


class StudentsList(View):

    def get(self, request):
        students = Student.objects.all().order_by('id')
        pageid = request.GET.get('page', 1)
        pages = Paginator(students, 20)
        try:
            page_students = pages.page(pageid)
        except PageNotAnInteger:
            page_students = pages.page(1)
        except EmptyPage:
            page_students = pages.page(pages.num_pages)
        return render(request, 'students.html', {'students': page_students})


class StudentEditView(View):
    form = StudentFormFromModel

    def get(self, request, id):
        student = Student.objects.get(id=id)
        form = self.form(instance=student)
        return render(request,
                      'edit_student_form.html',
                      {'form': form, 'id': id})

    def post(self, request, id):
        form = self.form(request.POST)
        if form.is_valid():
            Student.objects.update_or_create(
                                             defaults=form.cleaned_data,
                                             id=id)

            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            name = f'{firstname} {lastname}'

            messages.success(request, f'Student {name} saved')
            return redirect('students-list')
        else:
            return render(request,
                          'edit_student_form.html',
                          {'form': form, 'id': id})


class StudentAddView(View):

    def get(self, request):
        form = AddStudentForm()
        return render(request, 'add_student_form.html', {'form': form})

    def post(self, request):
        form = AddStudentForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            student = Student.objects.create(**formdata)
            name = f'{student.firstname} {student.lastname}'
            messages.success(request, f'Student {name} Added')
            return redirect('students-list')


class StudentDeleteView(View):

    def get(self, request, id):
        student = Student.objects.get(id=id)
        form = ConfirmActionForm()
        return render(request,
                      'delete_student_form.html',
                      {'form': form, 'student': student})

    def post(self, request, id):
        form = ConfirmActionForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data.get('btn')
            if choice == 'yes':
                student = Student.objects.get(id=id)
                name = f'{student.firstname} {student.lastname}'
                student.delete()
                messages.success(request, f'Student {name} Deleted')
        return redirect('students-list')
