from django.contrib import admin
from .models import RegistroHoras


@admin.register(RegistroHoras)
class RegistroHorasAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data', 'horas_trabalhadas')
    list_filter = ('usuario', 'data')
    search_fields = ('usuario__username',)