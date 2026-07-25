from django.contrib import admin
from .models import HorarioDisponivel, Agendamento


@admin.register(HorarioDisponivel)
class HorarioDisponiveladmin(admin.ModelAdmin):
    list_display = ('servico', 'data', 'hora_inicio', 'hora_fim', 'disponivel')
    list_filter = ('servico', 'data')
    search_fields = ('servico__nome',)
    readonly_fields = ('disponivel',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'horario_disponivel', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('usuario__username', 'horario_disponivel__servico__nome')
    readonly_fields = ('criado_em', 'atualizado_em')