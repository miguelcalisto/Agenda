from django.contrib import admin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.html import format_html

from clientes.models import Cliente
from produtos.models import Produto
from .models import Fornecedor

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'fone')
    search_fields = ('nome', 'fone')



