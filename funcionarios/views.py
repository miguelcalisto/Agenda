from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import FuncionarioModelForm
from .models import Funcionario

class FuncionariosView(ListView):
    model = Funcionario
    template_name = 'funcionarios.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(FuncionariosView, self).get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Não existem funcionários cadastrados!')
            return qs.none()


class FuncionarioAddView(SuccessMessageMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário cadastrado com sucesso!'



class FuncionarioUpdateView(SuccessMessageMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário alterado com sucesso!'


class FuncionarioDeleteView(SuccessMessageMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario_apagar.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário excluído com sucesso!'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                message=f'O funcionário {self.object} não pode ser excluído. '
                        f'Esse funcionário está registrado em agendamentos e/ou ordens de serviço'
            )
        finally:
            return redirect(success_url)

