from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Agendamento

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('horario', 'cliente', 'funcionario', 'valor')
    search_fields = ('cliente', 'funcionario')
    list_filter = ('cliente', 'servico')
