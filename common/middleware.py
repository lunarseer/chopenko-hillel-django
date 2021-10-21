from time import time

import re

from students.views import StudentAddView, StudentEditView
from teachers.views import TeacherAddView, TeacherEditView
from .models import LogRecord


PHONE_VIEWS = [TeacherAddView,
               TeacherEditView,
               StudentAddView,
               StudentEditView
               ]


class PhoneFieldFormatterMiddleware:
    """
    formatter for phone number field for addperson & editperson fields
    """
    def __init__(self, get_responce) -> None:
        self.get_responce = get_responce

    def __call__(self, request):
        responce = self.get_responce(request)
        return responce

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func in PHONE_VIEWS and request.method == 'POST':
            phone = request.POST.get('phone')
            post = request.POST.copy()
            post['phone'] = phone.strip('')


class AdminLogMiddleware:
    """
    writes log to database
    request.path
    request.method
    execution_time
    """
    def __init__(self, get_responce) -> None:
        self.get_responce = get_responce

    def __call__(self, request):
        start_time = time()
        responce = self.get_responce(request)
        elapsed_time = time() - start_time
        if re.search('admin', request.path):
            LogRecord.objects.create(path=request.path,
                                     method=request.method,
                                     execution_time=elapsed_time
                                     )
        return responce
