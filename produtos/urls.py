from django.urls import path

from .views import ProdutosView, ProdutoAddView

urlpatterns = [
    path('produtos', ProdutosView.as_view(), name='produtos'),
    path('produto/adicionar/', ProdutoAddView.as_view(), name='produto_adicionar')

]
