from django.views import View
from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse
from . import models

class ListaProdutos(ListView):
    # QuerySet
    model = models.Produto

    # Somente isso já carrega o template
    template_name = 'produto/lista.html'

class DetalheProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetalheProduto')

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

