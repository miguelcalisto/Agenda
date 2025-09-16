from django import forms
from django.forms import inlineformset_factory

from .models import Servico
from .models import Servico, ProdutosServico


class ServicoModelForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco']

        error_messages = {
            'nome': {'required': 'O nome do serviço é um campo obrigatório', 'unique': 'Serviço já cadastrado'},
            'descricao': {'required': 'A descrição do serviço é um campo obrigatório'},
            'preco': {'required': 'O preço do serviço é um campo obrigatório'},
        }


ProdutosServicoInLine = inlineformset_factory(
    Servico, ProdutosServico, fk_name='servico',
    fields=('produto', 'quantidade'), extra=1, can_delete=True
)