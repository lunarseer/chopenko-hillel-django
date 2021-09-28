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
        self.template = 'edit_entity_form'
        self.redirect_url = 'teachers-list'


class TeacherAddView(GenericEntityAddView):

    def __init__(self):
        self.model = Teacher
        self.form = TeacherAddForm
        self.template = 'add_entity_form'
        self.redirect_url = 'teachers-list'


class TeacherDeleteView(GenericEntityDeleteView):

    def __init__(self):
        self.model = Teacher
        self.template = 'delete_entity_form'
        self.redirect_url = 'teachers-list'
