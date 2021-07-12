from django.views import View
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from . import models

class ListaProdutos(ListView):
    # QuerySet
    model = models.Produto
    # Somente isso já carrega o template
    template_name = 'produto/lista.html'
    # Os objetos dentro do template vão se chamar produtos - coleção
    context_object_name = 'produtos'
    # Quantos produtos vao aparecer por página
    paginate_by = 1

class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdiconarAoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AdiconarAoCarrinho')

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinho')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')

class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')

