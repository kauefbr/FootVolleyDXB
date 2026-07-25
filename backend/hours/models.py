from django.db import models
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class RegistroHoras(models.Model):
    """
    Controle interno de horas trabalhadas (pra staff).
    """
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="registros_horas",
        help_text="Funcionário"
    )
    data = models.DateField(help_text="Data do trabalho")
    horas_trabalhadas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Quantidade de horas (ex: 8.5)"
    )
    descricao = models.TextField(
        blank=True,
        help_text="Descrição do trabalho realizado"
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data"]
        verbose_name = "Registro de Horas"
        verbose_name_plural = "Registros de Horas"

    def __str__(self):
        return f"{self.usuario.username} - {self.data} ({self.horas_trabalhadas}h)"

    def clean(self):
        """
        Validações customizadas para RegistroHoras.
        """
        from datetime import date
        from django.core.exceptions import ValidationError
        errors = {}

        # Validação 1: horas_trabalhadas deve ser > 0
        if self.horas_trabalhadas is not None and self.horas_trabalhadas <= 0:
            errors['horas_trabalhadas'] = "Horas trabalhadas deve ser maior que 0."

        # Validação 2: data não pode ser no futuro
        if self.data and self.data > date.today():
            errors['data'] = "Não pode registrar horas em datas futuras."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Sobrescreve save() pra garantir que clean() é sempre chamado antes de salvar.
        """
        self.full_clean()
        super().save(*args, **kwargs)