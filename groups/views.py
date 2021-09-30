from django.db.models import Count

from .models import Group

from .forms import GroupAddForm, GroupFormFromModel

from common.views import (GenericEntityListView,
                          GenericEntityEditView,
                          GenericEntityAddView,
                          GenericEntityDeleteView
                          )


class GroupsListView(GenericEntityListView):

    def __init__(self):
        self.model = Group
        self.template_name = 'groups_view.html'

    def get_queryset(self):
        annotation = {'fkeycount': Count('students')}
        return Group.objects.annotate(**annotation).order_by('id')


class GroupEditView(GenericEntityEditView):

    def __init__(self):
        self.model = Group
        self.form = GroupFormFromModel
        self.template_name = 'edit_entity_form.html'
        self.redirect_url = 'groups-list'


class GroupAddView(GenericEntityAddView):

    def __init__(self):
        self.model = Group
        self.form = GroupAddForm
        self.template_name = 'add_entity_form.html'
        self.redirect_url = 'groups-list'


class GroupDeleteView(GenericEntityDeleteView):

    def __init__(self):
        self.model = Group
        self.template_name = 'delete_entity_form.html'
        self.redirect_url = 'groups-list'
