from django.contrib import admin

# Register your models here.

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'age', 'phone']
    list_filter = ['firstname', 'lastname']
    search_fields = ['lastname__startswith']
