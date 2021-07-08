from django.urls import path
from . import views

# name space para facilitar, na hora de chamar vai ser algo como produto:lista
app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DetalehProduto.as_view(), name='detalhe'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('adicionaraocarrinho/', views.AdiconarAoCarrinho.as_view(), name='adicionaraocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name='removerdocarrinho'),
    path('finalizar/', views.Finalizar.as_view(), name='finalizar'),
]
