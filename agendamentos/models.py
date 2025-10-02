from django.db import models

class Agendamento(models.Model):
    horario = models.DateTimeField(
        verbose_name='Horário',
        help_text='Data e hora do atendimento'
    )
    cliente = models.ForeignKey(
        to='clientes.Cliente',
        verbose_name='Cliente',
        help_text='Nome do cliente',
        on_delete=models.PROTECT
    )
    funcionario = models.ForeignKey(
        to='funcionarios.Funcionario',
        verbose_name='Funcionário',
        help_text='Nome do funcionário',
        on_delete=models.PROTECT
    )
    servico = models.ManyToManyField(
        to='servicos.Servico',
        verbose_name='Serviço',
        through='agendamentos.OrdemServicos'
    )

    valor = models.DecimalField(verbose_name='Valor total', max_digits=6, decimal_places=2, default=0.00)

    status = models.CharField(
        'Status',
        max_length=1,
        help_text='Status do agendamento',
        default='A'
    )

    @property
    def servicos(self):
        return OrdemServicos.objects.filter(agendamento=self)

    class Meta:
        verbose_name = 'Agendamento'
        permissions= (('fechar_agendamento', 'Permite fazer o fechar  de um agendamento'),)
        verbose_name_plural = 'Agendamentos'
        ordering = ['-horario']

    def __str__(self):
        return f'Cliente: {self.cliente}'



from django.db import models

class OrdemServicos(models.Model):
    SITUACAO_OPCOES = (
        ('A', 'Agendado'),
        ('R', 'Realizado'),
        ('C', 'Cancelado'),
    )

    agendamento = models.ForeignKey(
        to='agendamentos.Agendamento',
        verbose_name='Agendamento',
        on_delete=models.CASCADE,
        related_name='ordens_servico'
    )
    servico = models.ForeignKey(
        to='servicos.Servico',
        verbose_name='Serviço',
        on_delete=models.PROTECT,
        related_name='ordens_servico'
    )
    funcionario = models.ForeignKey(
        to='funcionarios.Funcionario',
        verbose_name='Funcionário',
        on_delete=models.PROTECT,
        related_name='ordens_servico'
    )
    situacao = models.CharField(
        verbose_name='Situação',
        max_length=1,
        choices=SITUACAO_OPCOES,
        default='A'
    )
    observacoes = models.TextField(
        verbose_name='Observações',
        max_length=300,
        blank=True,
        null=True
    )
    preco = models.DecimalField(
        verbose_name='Preço',
        max_digits=6,
        decimal_places=2,
        help_text='Preço do serviço',
        default=0.00
    )

    def calcular_valor_ordem(self):
        valor_total = 0
        qs = OrdemServicos.objects.filter(agendamento=self.agendamento)
        for item in qs:
            if item.situacao != 'C':
                valor_total += item.preco
        self.agendamento.valor = valor_total
        self.agendamento.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.preco = self.servico.preco
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        self.calcular_valor_ordem()

    def delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)
        self.calcular_valor_ordem()

    class Meta:
        verbose_name = 'Serviço realizado'
        verbose_name_plural = 'Serviços realizados'
        constraints = [
            models.UniqueConstraint(
                fields=['agendamento', 'servico'],
                name='constraint_agendamento'
            )
        ]

    def __str__(self):
        return self.servico.nome

