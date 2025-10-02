from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q, ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.views.generic.base import TemplateResponseMixin

from servicos.forms import ServicoModelForm, ProdutosServicoInLine
from servicos.models import Servico


class ServicosView(PermissionRequiredMixin,ListView):
    permission_required = 'servicos.delete_servicos'
    permission_denied_message = 'ver servicos'

    model = Servico
    template_name = 'servicos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ServicosView, self).get_queryset()

        if buscar:
            qs = qs.filter(Q(nome__icontains=buscar) | Q(descricao__icontains=buscar))

        if qs.count() > 0:
            paginator = Paginator(qs, per_page=1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Não existem serviços cadastrados!')
            return qs.none()  # Retorna queryset vazio para evitar erros


class ServicoAddView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'servicos.add_servicos'
    permission_denied_message = 'add servicos'

    model = Servico
    form_class = ServicoModelForm
    template_name = 'servico_form.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Serviço cadastrado com sucesso!'


class ServicoUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'servicos.update_servicos'
    permission_denied_message = 'att servicos'

    model = Servico
    form_class = ServicoModelForm
    template_name = 'servico_form.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Serviço alterado com sucesso!'


class ServicoDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'servicos.delete_servicos'
    permission_denied_message = 'del servicos'

    model = Servico
    template_name = 'servico_apagar.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Serviço apagado com sucesso!'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request,
                           message=(
                               f'O serviço {self.object} não pode ser excluído. '
                               f'Esse serviço está registrado em ordens de serviço'
                           )
                           )
        finally:
            return redirect(success_url)


class ServicoInLineEditView(TemplateResponseMixin, View):
    template_name = 'servico_form_inline.html'

    def get_formset(self, data=None):
        return ProdutosServicoInLine(instance=self.servico, data=data)

    def dispatch(self, request, *args, **kwargs):
        self.servico = get_object_or_404(Servico, id=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'servico': self.servico, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('servicos')
        return self.render_to_response({'servico': self.servico, 'formset': formset})


# slide 15<