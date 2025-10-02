from django.contrib import admin

from servicos.models import Servico, ProdutosServico
from produtos.models import Produto
# Register your models here.

class ProdutoServicoInline(admin.TabularInline):
    model = ProdutosServico
    extra = 1

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco', 'get_produtos')
    inlines = [ProdutoServicoInline]
    search_fields = ('nome', 'descricao')

    def get_produtos(self, obj):
        return ', '.join([prd.nome for prd in Produto.objects.filter(servico=obj.id)])

    get_produtos.short_description = 'Produtos utilizados'
