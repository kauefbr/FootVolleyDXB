from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from services.models import Servico

Usuario = get_user_model()


class HorarioDisponivel(models.Model):
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name="horarios_disponiveis",
        help_text="Qual serviço é oferecido neste horário"
    )
    data = models.DateField(help_text="Data do horário")
    hora_inicio = models.TimeField(help_text="Hora de início (ex: 10:00)")
    hora_fim = models.TimeField(help_text="Hora de término (ex: 11:00)")

    class Meta:
        ordering = ["data", "hora_inicio"]
        unique_together = ("servico", "data", "hora_inicio")
        verbose_name = "Horário Disponível"
        verbose_name_plural = "Horários Disponíveis"
        # ===== ÍNDICES =====
        indexes = [
            models.Index(fields=['servico'], name='idx_horario_servico'),
            models.Index(fields=['data'], name='idx_horario_data'),
            models.Index(fields=['servico', 'data'], name='idx_horario_servico_data'),
        ]

    def __str__(self):
        return f"{self.servico.nome} - {self.data} ({self.hora_inicio})"

    def clean(self):
        """
        Validações customizadas para HorarioDisponivel.
        """
        errors = {}

        # Validação 1: hora_inicio deve ser menor que hora_fim
        if self.hora_inicio and self.hora_fim:
            if self.hora_inicio >= self.hora_fim:
                errors['hora_inicio'] = "Hora de início deve ser antes da hora de término."

        # Validação 2: data não pode ser no passado
        if self.data and self.data < date.today():
            errors['data'] = "Não pode criar horários em datas passadas."

        if errors:
            raise ValidationError(errors)

    @property
    def disponivel(self):
        """
        Calcula se este horário está disponível.
        Retorna True se NÃO existe um Agendamento confirmado para este horário.
        """
        return not self.agendamentos.filter(
            status__in=["confirmado", "pendente"]
        ).exists()


class Agendamento(models.Model):
    """
    Registra quando um cliente agendou um horário.
    """
    
    class StatusChoices(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        CONFIRMADO = "confirmado", "Confirmado"
        CANCELADO = "cancelado", "Cancelado"

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="agendamentos",
        help_text="Cliente que fez o agendamento"
    )
    horario_disponivel = models.ForeignKey(
        HorarioDisponivel,
        on_delete=models.CASCADE,
        related_name="agendamentos",
        help_text="Horário que foi reservado"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDENTE,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        # ===== ÍNDICES =====
        indexes = [
            models.Index(fields=['usuario'], name='idx_agendamento_usuario'),
            models.Index(fields=['status'], name='idx_agendamento_status'),
            models.Index(fields=['usuario', 'status'], name='idx_agendamento_usuario_status'),
            models.Index(fields=['horario_disponivel'], name='idx_agendamento_horario'),
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.horario_disponivel.servico.nome} ({self.status})"

    def clean(self):
        """
        Validações customizadas para Agendamento.
        """
        errors = {}

        # Validação 1: Verificar se ESTE ALUNO já marcou este horário
        if self.horario_disponivel and self.usuario:
            agendamentos_duplicados = Agendamento.objects.filter(
                usuario=self.usuario,
                horario_disponivel=self.horario_disponivel,
                status__in=["confirmado", "pendente"]
            ).exclude(pk=self.pk)
            
            if agendamentos_duplicados.exists():
                errors['horario_disponivel'] = "Você já marcou este horário. Não é possível marcar duas vezes."

        # Validação 2: Verificar se a data do horário é no passado
        if self.horario_disponivel and self.horario_disponivel.data < date.today():
            errors['horario_disponivel'] = "Não pode agendar em horários com data no passado."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Sobrescreve save() pra garantir que clean() é sempre chamado antes de salvar.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    # ===== MÉTODOS CUSTOMIZADOS =====

    def pode_cancelar(self):
        """
        Verifica se este agendamento pode ser cancelado.
        Regra: só pode cancelar se status for "pendente" ou "confirmado".
        """
        return self.status in ["pendente", "confirmado"]

    def cancelar(self):
        """
        Cancela o agendamento (muda status pra cancelado).
        Só funciona se pode_cancelar() retornar True.
        """
        if self.pode_cancelar():
            self.status = "cancelado"
            self.save()
            return True
        return False

    def hora_completa(self):
        """
        Retorna data + hora formatada: "24/07/2026 20:00"
        """
        data_formatada = self.horario_disponivel.data.strftime("%d/%m/%Y")
        hora_formatada = self.horario_disponivel.hora_inicio.strftime("%H:%M")
        return f"{data_formatada} {hora_formatada}"

    def esta_confirmado(self):
        """
        Retorna True se o agendamento está confirmado.
        """
        return self.status == "confirmado"

    def dias_ate_agendamento(self):
        """
        Retorna quantos dias faltam até o agendamento.
        """
        diferenca = self.horario_disponivel.data - date.today()
        return diferenca.days
