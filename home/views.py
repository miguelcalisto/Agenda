from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
"""
def index(request):
    context = {
        'disciplina': 'Desenvolvimento Web - Técnico em Informática - Politécnico - UFSM',
        'tecnologia': 'Python e Django',
    }

    return render(request, 'index.html', context)
"""

class IndexView(TemplateView):
    template_name = 'index.html'