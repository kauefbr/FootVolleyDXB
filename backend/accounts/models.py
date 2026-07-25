from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Estende o usuário padrão do Django.
    Já vem com: username, email, password (hash), first_name, last_name,
    is_staff, is_active, date_joined, etc.
    """

    class Tipo(models.TextChoices):
        CLIENTE = "cliente", "Cliente"
        STAFF = "staff", "Staff"

    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices,
        default=Tipo.CLIENTE,
    )
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username

    # ===== MÉTODOS CUSTOMIZADOS =====

    def agendamentos_confirmados(self):
        """
        Retorna queryset de todos os agendamentos confirmados deste usuário.
        """
        return self.agendamentos.filter(status="confirmado")

    def proximos_agendamentos(self):
        """
        Retorna agendamentos futuros (data >= hoje) ordenados por data.
        """
        from datetime import date
        return self.agendamentos.filter(
            horario_disponivel__data__gte=date.today(),
            status__in=["pendente", "confirmado"]
        ).order_by("horario_disponivel__data")

    def ultimo_agendamento(self):
        """
        Retorna o agendamento mais recente (ou None se não tiver nenhum).
        """
        return self.agendamentos.first()

    def total_aulas_confirmadas(self):
        """
        Retorna quantas aulas/serviços este usuário confirmou.
        """
        return self.agendamentos_confirmados().count()

    def eh_cliente(self):
        """
        Verifica se o usuário é cliente (não staff).
        """
        return self.tipo == "cliente"

    def eh_staff(self):
        """
        Verifica se o usuário é staff (funcionário).
        """
        return self.tipo == "staff"