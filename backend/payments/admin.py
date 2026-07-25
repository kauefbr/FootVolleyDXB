from django.contrib import admin
from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('agendamento', 'valor', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('agendamento__usuario__username',)
    readonly_fields = ('stripe_payment_id', 'criado_em', 'atualizado_em')