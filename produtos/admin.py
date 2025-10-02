from django.contrib import admin

from produtos.models import Produto


# Register your models here.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade', 'fornecedor')
    search_fields = ('nome',)
    list_filter = ('fornecedor',)
