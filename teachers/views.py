from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import Teacher

from .forms import AddTeacherForm, TeacherFormFromModel


# Create your views here.


def teachers_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers.html', {'teachers': teachers})


def get_teacher(request, teacher_id):
    student = Teacher.objects.get(id=teacher_id)
    return HttpResponse(status=200, content=student)


def edit_teacher(request, teacher_id):

    def render_edit_form(form):
        return render(request,
                      'edit_teacher_form.html',
                      {'form': form, 'teacher_id': teacher_id})

    if request.method == "POST":
        form = TeacherFormFromModel(request.POST)
        if form.is_valid():
            Teacher.objects.update_or_create(defaults=form.cleaned_data,
                                             id=teacher_id)
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            name = f'{firstname} {lastname}'

            messages.success(request, f'Teacher {name} saved')
            return redirect('teachers-list')
        else:
            return render_edit_form(form)
    else:
        teacher = Teacher.objects.get(id=teacher_id)
        form = TeacherFormFromModel(instance=teacher)
        return render_edit_form(form)


def add_teacher(request):
    if request.method == "POST":
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            Teacher.objects.create(**formdata)
            return redirect('teachers-list')
    else:
        form = AddTeacherForm()
    return render(request, 'add_teacher_form.html', {'form': form})


def delete_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    name = f'{teacher.firstname} {teacher.lastname}'
    messages.success(request, f'Teacher {name} Deleted')
    teacher.delete()
    return redirect('teachers-list')
