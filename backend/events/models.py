from django.db import models

class Evento(models.Model):
    """
    Calendário de eventos (palestras, workshops, férias da empresa, etc.)
    """
    
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    data = models.DateField(help_text="Data do evento")
    data_fim = models.DateField(
        blank=True,
        null=True,
        help_text="Data de término (se for um evento com duração)"
    )
    link_interativo = models.URLField(
        blank=True,
        help_text="Link pra mais informações (ex: Zoom, formulário, etc.)"
    )
    ativo = models.BooleanField(
        default=True,
        help_text="Eventos inativos não aparecem no calendário"
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["data"]
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return f"{self.nome} ({self.data})"