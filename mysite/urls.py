from django.contrib import admin
from django.urls import path, include

from common.views import Error

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('common.urls')),
    path('', include('students.urls')),
    path('', include('teachers.urls')),
    path('', include('groups.urls')),
]

GlobalErrorHandler = Error()

handler400 = GlobalErrorHandler.error_400
handler403 = GlobalErrorHandler.error_403
handler404 = GlobalErrorHandler.error_404
handler500 = GlobalErrorHandler.error_500
