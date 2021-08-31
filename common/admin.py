from django.contrib import admin

# Register your models here.

from .models import LogRecord


@admin.register(LogRecord)
class CommonAdmin(admin.ModelAdmin):
    list_display = ['method', 'path', 'created', 'execution_time']
    list_filter = ['path', 'method']
    # search_fields = ['lastname__startswith']
