from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Teacher

from .forms import AddTeacherForm


# Create your views here.


def add_teacher(request):
    if request.method == "POST":
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            person = Teacher.objects.create(firstname=formdata['firstname'],
                                            lastname=formdata['lastname'],
                                            age=formdata['age'])
            entitylist = [f"{person.firstname} {person.lastname}"]
            data = {'message': '1 teacher created', 'entitylist': entitylist}
            return render(request, 'entity_responce.html', data)
    else:
        form = AddTeacherForm()
    return render(request, 'add_teacher_form.html', {'form': form})


def get_teachers(request):
    query = {q: v for q, v in request.GET.items()}
    try:
        response = [x.values() for x in Teacher.objects.filter(**query)]
    except Exception as e:
        return JsonResponse(status=404, data={"message": str(e)})
    return JsonResponse(status=200, data=response, safe=False)