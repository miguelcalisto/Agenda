from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'disciplina': 'Desenvolvimento Web - Técnico em Informática - Politécnico - UFSM',
        'tecnologia': 'Python e Django',
    }

    return render(request, 'index.html', context)
