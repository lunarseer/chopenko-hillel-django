from django.contrib import admin

# Register your models here.

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'age', 'phone', 'disciplines']
    list_filter = ['firstname', 'lastname']
    search_fields = ['lastname__startswith']
