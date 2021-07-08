from django.views import View
from django.shortcuts import render
from django.views.generic.list import ListView

# Create your views here.

class ListaProdutos(ListView):
    pass

class DetalheProduto(View):
    pass

class AdiconarAoCarrinho(View):
    pass

class RemoverDoCarrinho(View):
    pass

class Finalizar(View):
    pass

class Carrinho(View):
    pass

