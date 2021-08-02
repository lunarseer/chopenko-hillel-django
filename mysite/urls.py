"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from students import views as stud

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate-student/', stud.generate_student),
    path('generate-students/', stud.generate_students),
    path('generate-teachers/', stud.generate_teachers),
    path('generate-groups/', stud.generate_groups),
    path('students/', stud.get_students),
    path('groups/', stud.get_groups),
    path('teachers/', stud.get_teachers),
]
