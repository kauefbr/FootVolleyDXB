import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_institucional.settings')
django.setup()

from booking.models import Agendamento
from django.db import connection
from django.test.utils import CaptureQueriesContext

print("=" * 60)
print("TESTE 1: SEM select_related (N+1 - LENTO)")
print("=" * 60)

with CaptureQueriesContext(connection) as context:
    agendamentos = Agendamento.objects.all()
    for agendamento in agendamentos:
        _ = agendamento.usuario.username
        _ = agendamento.horario_disponivel.servico.nome

print(f"Total de queries: {len(context.captured_queries)}\n")

print("=" * 60)
print("TESTE 2: COM select_related (RÁPIDO)")
print("=" * 60)

with CaptureQueriesContext(connection) as context:
    agendamentos = Agendamento.objects.select_related(
        'usuario',
        'horario_disponivel__servico'
    )
    for agendamento in agendamentos:
        _ = agendamento.usuario.username
        _ = agendamento.horario_disponivel.servico.nome

print(f"Total de queries: {len(context.captured_queries)}\n")

print("=" * 60)
print("RESULTADO ESPERADO:")
print("Teste 1 deve ter MUITO mais queries que Teste 2")
print("=" * 60)