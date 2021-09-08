from django.contrib import admin

# Register your models here.

from .models import NbuCurrency, LogRecord, MonoCurrency


@admin.register(LogRecord)
class LogAdmin(admin.ModelAdmin):
    list_display = ['method', 'path', 'created', 'execution_time']
    list_filter = ['path', 'method']


@admin.register(MonoCurrency)
class MonoAdmin(admin.ModelAdmin):
    pass
    # list_display = ['method', 'path', 'created', 'execution_time']
    # list_filter = ['path', 'method']
    # search_fields = ['lastname__startswith']


@admin.register(NbuCurrency)
class NbuAdmin(admin.ModelAdmin):
    pass
    # list_display = ['method', 'path', 'created', 'execution_time']
    # list_filter = ['path', 'method']
    # search_fields = ['lastname__startswith']


