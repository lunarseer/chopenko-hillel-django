from .models import Teacher

from .forms import TeacherAddForm, TeacherFormFromModel


from common.views import (GenericEntityListView,
                          GenericEntityEditView,
                          GenericEntityAddView,
                          GenericEntityDeleteView
                          )


# Create your views here.


class TeachersListView(GenericEntityListView):

    def __init__(self):
        self.model = Teacher
        self.template_name = 'entities_view.html'


class TeacherEditView(GenericEntityEditView):

    def __init__(self):
        self.model = Teacher
        self.form = TeacherFormFromModel
        self.template_name = 'edit_entity_form.html'
        self.redirect_url = 'teachers-list'


class TeacherAddView(GenericEntityAddView):

    def __init__(self):
        self.model = Teacher
        self.form = TeacherAddForm
        self.template_name = 'add_entity_form.html'
        self.redirect_url = 'teachers-list'


class TeacherDeleteView(GenericEntityDeleteView):

    def __init__(self):
        self.model = Teacher
        self.template_name = 'delete_entity_form.html'
        self.redirect_url = 'teachers-list'
