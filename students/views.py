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
        self.template_name = 'entities_view.html'


class StudentEditView(GenericEntityEditView):

    def __init__(self):
        self.model = Student
        self.form = StudentFormFromModel
        self.template_name = 'edit_entity_form.html'
        self.redirect_url = 'students-list'


class StudentAddView(GenericEntityAddView):

    def __init__(self):
        self.model = Student
        self.form = StudentAddForm
        self.template = 'add_entity_form'
        self.redirect_url = 'students-list'


class StudentDeleteView(GenericEntityDeleteView):

    def __init__(self):
        self.model = Student
        self.template = 'delete_entity_form'
        self.redirect_url = 'students-list'
