from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

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
            group_name = formdata['name']
            Group.objects.create(name=group_name,
                                 discipline=formdata['discipline'])
            messages.success(request, f'Group {group_name} added')
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
            name = form.cleaned_data.get('name', '')
            messages.success(request, f'Group {name} Saved')
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
    name = group.name
    group.delete()
    messages.success(request, f'Group {name} deleted')
    return redirect('groups-list')
