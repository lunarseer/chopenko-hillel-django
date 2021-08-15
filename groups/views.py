from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Group
from students.models import Student
from teachers.models import Teacher

from .forms import AddGroupForm, GroupFormFromModel


# Create your views here.


def groups_list(request):
    groups = Group.objects.all()
    return render(request, 'groups.html', {'groups': groups})


def get_group(request, group_id):
    group = Group.objects.get(id=group_id)
    return HttpResponse(status=200, content=group)


def add_group(request):
    if not all([Student.objects.all(), Teacher.objects.all()]):
        return HttpResponse("Add Students and Teachers first")
    if request.method == "POST":
        form = AddGroupForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            Group.objects.create(name=formdata['name'],
                                 discipline=formdata['discipline'])
            return redirect('groups-list')
        else:
            return HttpResponse('Invalid Form', form.fields)
    else:
        form = AddGroupForm()
    return render(request, 'add_group_form.html', {'form': form})


def edit_group(request, group_id):
    if request.method == "POST":
        form = GroupFormFromModel(request.POST)
        if form.is_valid():
            Group.objects.update_or_create(
                                           defaults=form.cleaned_data,
                                           id=group_id)
            return redirect('groups-list')
    else:
        group = Group.objects.get(id=group_id)
        form = GroupFormFromModel(instance=group)
        return render(
                      request,
                      'edit_group_form.html',
                      {'form': form, 'group_id': group_id})


def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    return redirect('groups-list')
