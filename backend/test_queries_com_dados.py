import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_institucional.settings')
django.setup()

from booking.models import Agendamento, HorarioDisponivel
from services.models import Servico
from accounts.models import Usuario
from django.db import connection
from django.test.utils import CaptureQueriesContext
from datetime import date, time

print("Criando dados de teste...")

# Criar 5 usuários diferentes
usuarios = []
for i in range(5):
    try:
        u = Usuario.objects.create_user(
            username=f"usuario_{i}",
            email=f"user{i}@test.com",
            password="123456",
            tipo="cliente"
        )
        usuarios.append(u)
    except:
        pass

# Criar 3 serviços diferentes
servicos = []
for i in range(3):
    try:
        s = Servico.objects.create(
            nome=f"Serviço {i}",
            duracao_minutos=60,
            preco=100.0 + i,
            ativo=True
        )
        servicos.append(s)
    except:
        pass

# Criar horários e agendamentos
contador = 0
for servico in servicos:
    for i in range(5):
        try:
            h = HorarioDisponivel.objects.create(
                servico=servico,
                data=date(2026, 8, 1 + contador),
                hora_inicio=time(10, 0),
                hora_fim=time(11, 0)
            )
            # Criar agendamento com usuário diferente
            usuario = usuarios[i % len(usuarios)]
            Agendamento.objects.create(
                usuario=usuario,
                horario_disponivel=h,
                status="confirmado"
            )
            contador += 1
        except:
            pass

print(f"Total de agendamentos criados: {Agendamento.objects.count()}\n")

# AGORA SIM os testes
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
if len(context.captured_queries) == 1:
    print("✅ RESULTADO: select_related é MUITO mais rápido!")
else:
    print("Diferença demonstrada acima")
print("=" * 60)

