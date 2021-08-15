from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .models import Teacher

from .forms import AddTeacherForm, TeacherFormFromModel


# Create your views here.


def teachers_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers.html', {'teachers': teachers})


def get_teacher(request):
    query = {q: v for q, v in request.GET.items()}
    try:
        response = [x.values() for x in Teacher.objects.filter(**query)]
    except Exception as e:
        return JsonResponse(status=404, data={"message": str(e)})
    return JsonResponse(status=200, data=response, safe=False)


def edit_teacher(request, teacher_id):
    if request.method == "POST":
        form = TeacherFormFromModel(request.POST)
        if form.is_valid():
            Teacher.objects.update_or_create(defaults=form.cleaned_data, id=teacher_id)
            return redirect('teachers-list')
    else:
        
        teacher = Teacher.objects.get(id=teacher_id)
        form = TeacherFormFromModel(instance=teacher)
        return render(request, 'edit_teacher_form.html', {'form': form, 'teacher_id': teacher_id})


def add_teacher(request):
    if request.method == "POST":
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            person = Teacher.objects.create(firstname=formdata['firstname'],
                                            lastname=formdata['lastname'],
                                            age=formdata['age'])
            return redirect('teachers-list')
    else:
        form = AddTeacherForm()
    return render(request, 'add_teacher_form.html', {'form': form})


def delete_teacher(request, teacher_id):
    pass


