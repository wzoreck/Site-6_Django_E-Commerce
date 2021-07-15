from . import models
from django.views import View
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render, redirect, reverse, get_list_or_404

class ListaProdutos(ListView):
    # QuerySet
    model = models.Produto
    # Somente isso já carrega o template
    template_name = 'produto/lista.html'
    # Os objetos dentro do template vão se chamar produtos - coleção
    context_object_name = 'produtos'
    # Quantos produtos vao aparecer por página
    paginate_by = 8

class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdiconarAoCarrinho(View):
    def get(self, *args, **kwargs):
        '''
            Desta forma conseguimos voltar para a URL anterior sem presicar informar explicitamente ela,
            ou seja continuar na mesma URL.
            Pois queremos apenas adicionar ao carrinho! Ao clickar no botão queremos o comportamento de 
            adicionar ao carrinho e permanecer na mesma página.

            return redirect(self.request.META['HTTP_REFERER'])
        '''

        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não possui variação'
            )
            return redirect(http_referer)
        
        # Tenta obter o objeto, caso contrário levanta erro 404
        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        # Trabalhando com a sessão do Django, tentando obter a chave carrinho da sessão, caso não exista criamos
        if not self.request.session.get('carrinho'):
            # Criando a chave carrinho no dicionário da sessão do usuário
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            # TODO: Variação existe no carrinho
            pass
        else:
            pass 

        return HttpResponse(f'{variacao.produto} - {variacao.nome}')

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinho')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')

class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')

