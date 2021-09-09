from django.contrib import admin

# Register your models here.

from .models import NbuCurrency, LogRecord, MonoCurrency


@admin.register(LogRecord)
class LogAdmin(admin.ModelAdmin):
    list_display = ['method', 'path', 'created', 'execution_time']
    list_filter = ['path', 'method']


@admin.register(MonoCurrency)
class MonoAdmin(admin.ModelAdmin):
    list_display = ['created', 'rate_usd', 'rate_eur']


@admin.register(NbuCurrency)
class NbuAdmin(admin.ModelAdmin):
    list_display = ['created', 'rate_usd', 'rate_eur']
