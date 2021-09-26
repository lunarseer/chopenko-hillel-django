from os import getenv
from dotenv import load_dotenv

from django.core.management import call_command

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View


from .forms import GeneratorCountForm, ContactForm
from .tasks import send_mail_message
from .models import CurrencyStamp


load_dotenv()


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class CurrencyView(View):
    def get(self, request):
        stamps = CurrencyStamp.objects.all()
        return render(request,
                      'currencies.html',
                      {'stamps': stamps}
                      )


class FakeGeneratorView(View):
    def get(self, request):
        return render(request, 'fake_generator.html', {})


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
