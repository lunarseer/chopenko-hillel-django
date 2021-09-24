from django.contrib import admin

# Register your models here.

from .models import CurrencyStamp, LogRecord


@admin.register(LogRecord)
class LogAdmin(admin.ModelAdmin):
    list_display = ['method', 'path', 'created', 'execution_time']
    list_filter = ['path', 'method']


@admin.register(CurrencyStamp)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['created', 'currency', 'bank', 'exchangerate']
