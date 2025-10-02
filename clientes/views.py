from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.checks import messages
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ClienteModelForm
# Create your views here.
from .models import Cliente

class ClientesView(PermissionRequiredMixin ,ListView):
    permission_required = 'clientes.view_cliente'
    permission_denied_message = 'Visualizar cliente'

    model = Cliente
    template_name = 'clientes.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ClientesView, self).get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, per_page=1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, message='Não existem clientes cadastrados!')

class ClienteAddView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'clientes.add_cliente'
    permission_denied_message = 'Cadastrar cliente'

    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente cadastrado com sucesso!'

class ClienteUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'clientes.update_cliente'
    permission_denied_message = 'Editar cliente'

    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente alterado com sucesso!'


class ClienteDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'clientes.delete_cliente'
    permission_denied_message = 'Excluir cliente'

    model = Cliente
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente excluido com sucesso!'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                message=f'O cliente {self.object} não pode ser excluído. '
                        f'Esse cliente está registrado em agendamentos'
            )
        finally:
            return redirect(success_url)

