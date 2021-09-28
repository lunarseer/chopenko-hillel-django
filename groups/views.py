from django.db.models import Count

from .models import Group
from teachers.models import Teacher

from .forms import GroupAddForm, GroupFormFromModel

from common.views import (GenericEntityListView,
                          GenericEntityEditView,
                          GenericEntityAddView,
                          GenericEntityDeleteView
                          )



# Create your views here.


class GroupsListView(GenericEntityListView):

    def __init__(self):
        self.model = Group
        self.template_name = 'entities_view.html'

    def get_queryset(self):
        annotation = {'fkeycount': Count('students')}
        return Group.objects.annotate(**annotation).order_by('id')


class GroupEditView(GenericEntityEditView):

    def __init__(self):
        self.model = Group
        self.form = GroupFormFromModel
        self.template = 'edit_entity_form'
        self.redirect_url = 'groups-list'


class GroupAddView(GenericEntityAddView):

    def __init__(self):
        self.model = Group
        self.form = GroupAddForm
        self.template = 'add_entity_form'
        self.redirect_url = 'groups-list'


class GroupDeleteView(GenericEntityDeleteView):

    def __init__(self):
        self.model = Group
        self.template = 'delete_entity_form'
        self.redirect_url = 'groups-list'