from django.contrib import admin
from .models import Evento


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data', 'data_fim', 'ativo')
    list_filter = ('ativo', 'data')
    search_fields = ('nome',)