from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.checks import messages
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from produtos.forms import ProdutoModelForm
from produtos.models import Produto


# Create your views here.
class ProdutosView(PermissionRequiredMixin,ListView):
    permission_required = 'produtos.view_produtos'
    permission_denied_message = 'ver produto'

    model = Produto
    template_name = 'produtos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ProdutosView, self).get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, per_page=1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, message='Não existem produtos cadastrados!')

class ProdutoAddView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'produtos.add_produtos'
    permission_denied_message = 'add produto'

    model = Produto
    form_class = ProdutoModelForm
    template_name = 'produto_form.html'
    success_url = reverse_lazy('produtos')
    success_message = 'Produto cadastrado com sucesso!'


class ProdutoUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'produtos.update_produtos'
    permission_denied_message = 'att produto'

    model = Produto
    form_class = ProdutoModelForm
    template_name = 'produto_form.html'
    success_url = reverse_lazy('produtos')
    success_message = 'Produto alterado com sucesso!'


class ProdutoDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'produtos.delete_produtos'
    permission_denied_message = 'del produto'

    model = Produto
    template_name = 'produto_apagar.html'
    success_url = reverse_lazy('produtos')
    success_message = 'Produto apagado com sucesso!'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request,
                           message=(
                               f'O produto {self.object} não pode ser excluído. '
                               f'Esse produto é utilizado em serviços'
                           )
                           )
        finally:
            return redirect(success_url)
