from django.db import models
from booking.models import Agendamento
from django.core.exceptions import ValidationError

class Pagamento(models.Model):
    """
    Registra o pagamento de um agendamento via Stripe.
    """
    
    class StatusChoices(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        PROCESSANDO = "processando", "Processando"
        CONFIRMADO = "confirmado", "Confirmado"
        FALHOU = "falhou", "Falhou"
        REEMBOLSADO = "reembolsado", "Reembolsado"

    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.CASCADE,
        related_name="pagamento",
        help_text="Agendamento que este pagamento está vinculado"
    )
    valor = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Valor em reais"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDENTE,
    )
    stripe_payment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text="ID da transação no Stripe"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        # ===== ÍNDICES =====
        indexes = [
        models.Index(fields=['status'], name='idx_pagamento_status'),
        models.Index(fields=['agendamento'], name='idx_pagamento_agendamento'),
        ]
        # ===== CONSTRAINTS SQL =====
        constraints = [
            models.CheckConstraint(
            condition=models.Q(valor__gt=0),
            name='ck_pagamento_valor_positivo'
            ),
        ]
    def __str__(self):
        return f"Pagamento - {self.agendamento.usuario.username} ({self.status})"

    def clean(self):
        """
        Validações customizadas para Pagamento.
        """
        errors = {}

        # Validação 1: valor deve ser > 0
        if self.valor is not None and self.valor <= 0:
            errors['valor'] = "Valor deve ser maior que R$ 0,00."

        # Validação 2: valor deve corresponder ao preço do serviço
        if self.agendamento and self.valor != self.agendamento.horario_disponivel.servico.preco:
            errors['valor'] = f"Valor deve ser exatamente R$ {self.agendamento.horario_disponivel.servico.preco:.2f} (preço do serviço)."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Sobrescreve save() pra garantir que clean() é sempre chamado antes de salvar.
        """
        self.full_clean()
        super().save(*args, **kwargs)