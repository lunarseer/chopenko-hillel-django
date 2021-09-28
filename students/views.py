from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from .models import Student
from .forms import (StudentAddForm,
                    StudentFormFromModel,
                    )
from common.views import (GenericEntityListView,
                          GenericEntityEditView,
                          GenericEntityAddView,
                          GenericEntityDeleteView
                          )



# Create your views here.


class StudentsList(GenericEntityListView):

    def __init__(self):
        self.model = Student
        self.template = 'entities_view'


class StudentEditView(GenericEntityEditView):

    def __init__(self):
        self.model = Student
        self.form = StudentFormFromModel
        self.template = 'edit_entity_form'
        self.redirect_url = 'students-list'


class StudentAddView(GenericEntityAddView):

    def __init__(self):
        self.model = Student
        self.form = StudentAddForm
        self.template = 'add_entity_form'
        self.redirect_url = 'students-list'


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
