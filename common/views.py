from os import getenv
from dotenv import load_dotenv

from django.core.management import call_command

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, ListView

from .forms import GeneratorCountForm, ContactForm, ConfirmActionForm
from .tasks import send_mail_message
from .models import CurrencyStamp


load_dotenv()


class IndexView(TemplateView):
    template_name = 'index.html'


class CurrencyView(ListView):
    paginate_by = 20
    model = CurrencyStamp
    template_name = 'currencies.html'


class FakeGeneratorView(TemplateView):
    template_name = 'fake_generator.html'


class GenericEntityListView(ListView):
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = [x.name for x in self.model._meta.fields]
        context['type'] = self.model.__name__
        return context


class GenericEntityAddView(View):

    def get(self, request):
        return render(request,
                      self.template_name,
                      {'form': self.form(), 'type': self.model.__name__,})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            entity = self.model.objects.create(**formdata)
            messages.success(request, f'{entity.info} Added')
            return redirect(self.redirect_url)


class GenericEntityEditView(View):

    def get(self, request, id):
        entity = self.model.objects.get(id=id)
        form = self.form(instance=entity)
        return render(request,
                      self.template_name,
                      {'form': form, 'id': id, 'type': self.model.__name__})

    def post(self, request, id):
        form = self.form(request.POST)
        if form.is_valid():
            self.model.objects.update_or_create(
                                                defaults=form.cleaned_data,
                                                id=id)
            entity = self.model.objects.get(id=id)
            messages.success(request, f'{entity.info} saved')
            return redirect(self.redirect_url)
        else:
            return render(request,
                          '%s.html' % self.template,
                          {'form': form, 'id': id, 'type': self.model.__name__})


class GenericEntityDeleteView(View):


    def get(self, request, id):
        entity = self.model.objects.get(id=id)
        form = ConfirmActionForm()
        question = f'Delete {self.model.__name__} {entity}?'
        return render(request,
                      '%s.html' % self.template,
                      {'form': form,  'id': id, 'type': self.model.__name__, 'question': question})

    def post(self, request, id):
        form = ConfirmActionForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data.get('btn')
            if choice == 'yes':
                entity = self.model.objects.get(id=id)
                entity.delete()
                message = f'{self.model.__name__} {entity} Deleted'
                messages.success(request, message)
        return redirect(self.redirect_url)


class ContactUsView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact_us.html',
                      {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            send_to = [
                getenv('EMAIL_HOST_USER'),
                ]
            subject = form.cleaned_data.get('subject')
            send_from = form.cleaned_data.get('send_from')
            message = form.cleaned_data.get('message')
            send_mail_message.delay(send_to=send_to,
                                    subject=subject,
                                    send_from=send_from,
                                    message=message)
            messages.success(request, 'Email Sent.')
            return redirect('home')


class EntityGeneratorView(View):
    entitytype = 'generic'

    def get(self, request):
        form = GeneratorCountForm()
        entitytype = self.entitytype.capitalize()
        return render(request, 'generate_form.html',
                      {'form': form, 'entitytype': entitytype})

    def post(self, request):
        form = GeneratorCountForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data.get('count')
            call_command(f'generate_{self.entitytype}', count=count)
            msg = f'{count} {self.entitytype.capitalize()} Generated.'
            messages.success(request, msg)
            return redirect(f'{self.entitytype}-list')


class StudentsGeneratorView(EntityGeneratorView):

    def __init__(self):
        self.entitytype = 'students'


class TeachersGeneratorView(EntityGeneratorView):

    def __init__(self):
        self.entitytype = 'teachers'


class GroupsGeneratorView(EntityGeneratorView):
    def __init__(self):
        self.entitytype = 'groups'
