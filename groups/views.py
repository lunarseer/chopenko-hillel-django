from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .models import Group
from students.models import Student
from teachers.models import Teacher

from .forms import AddGroupForm


# Create your views here.

def add_group(request):
    if not all([Student.objects.all(), Teacher.objects.all()]):
        return HttpResponse("Add Students and Teachers first")
    if request.method == "POST":
        form = AddGroupForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            group = Group.objects.create(name=formdata['name'],
                                         discipline=formdata['discipline'])
            return redirect('groups-list')
        else:
            return HttpResponse('Invalid Form', form.fields)
    else:
        form = AddGroupForm()
    return render(request, 'add_group_form.html', {'form': form})


def get_groups(request):
    response = [x.values() for x in Group.objects.all()]
    return JsonResponse(status=200, data=response, safe=False)


def get_groups_list(request):
    groups = Group.objects.all()
    return render(request, 'groups.html', {'groups': groups})