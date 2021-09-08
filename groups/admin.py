from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.

from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'discipline', 'link_to_teacher', 'link_to_headman')
    list_filter = ('discipline', 'teacher')
    search_fields = ('discipline__startswith',)

    def link_to_teacher(self, obj):
        link = reverse("admin:teachers_teacher_change", args=[obj.teacher.id])
        return format_html('<a href="{}">{} {}</a>', link, obj.teacher.firstname, obj.teacher.lastname)
    link_to_teacher.short_description = 'Edit teacher'

    def link_to_headman(self, obj):
        link = reverse("admin:students_student_change", args=[obj.headman.id])
        return format_html('<a href="{}">{} {}</a>', link, obj.headman.firstname, obj.headman.lastname)
    link_to_headman.short_description = 'Edit headman'