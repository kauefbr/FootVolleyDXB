from django.db import models
from django.core.exceptions import ValidationError


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    duracao_minutos = models.PositiveIntegerField(
        help_text="Duração do serviço em minutos"
    )
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    ativo = models.BooleanField(
        default=True,
        help_text="Serviços inativos não aparecem para novos agendamentos",
    )

    class Meta:
        ordering = ["nome"]
     # ===== CONSTRAINTS SQL =====
        constraints = [
        models.CheckConstraint(
            condition=models.Q(preco__gt=0),
            name='ck_servico_preco_positivo'
        ),
        models.CheckConstraint(
            condition=models.Q(duracao_minutos__gt=0),
            name='ck_servico_duracao_positiva'
        ),
    ]

    def __str__(self):
        return self.nome

    def clean(self):
        """
        Validações customizadas do modelo Servico.
        Este método é chamado:
        - No admin Django (ao salvar)
        - Quando você chama .full_clean()
        - Em formulários Django
        
        Validações aqui garantem que os dados fazem sentido do ponto de vista de negócio.
        """
        errors = {}

        # Validação 1: duracao_minutos deve ser > 0
        if self.duracao_minutos is not None and self.duracao_minutos <= 0:
            errors['duracao_minutos'] = "Duração deve ser maior que 0 minutos."

        # Validação 2: preco deve ser > 0
        if self.preco is not None and self.preco <= 0:
            errors['preco'] = "Preço deve ser maior que R$ 0,00."

        # Se houver erros, levanta exceção com todos eles
        if errors:
            raise ValidationError(errors)

    # ===== MÉTODOS CUSTOMIZADOS =====

    def preco_formatado(self):
        """
        Retorna o preço formatado como string: "R$ 100,00"
        Útil pra exibir no frontend sem ter que formatar lá.
        """
        return f"R$ {self.preco:.2f}"

    def duracao_formatada(self):
        """
        Converte minutos em formato legível: "1h 30min"
        Ex: 90 minutos → "1h 30min"
             60 minutos → "1h"
             30 minutos → "30min"
        """
        horas = self.duracao_minutos // 60  # Divisão inteira
        minutos = self.duracao_minutos % 60  # Resto da divisão

        if horas == 0:
            return f"{minutos}min"
        elif minutos == 0:
            return f"{horas}h"
        else:
            return f"{horas}h {minutos}min"

    def quantidade_agendamentos(self):
        """
        Retorna quantas vezes este serviço foi agendado (só confirmados).
        """
        return self.agendamentos.filter(status="confirmado").count()