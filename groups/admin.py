from django.contrib import admin

# Register your models here.

from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'discipline']
    list_filter = ['name', 'discipline']
    search_fields = ['discipline__startswith']
