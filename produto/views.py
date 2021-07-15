from . import models
from django.views import View
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render, redirect, reverse, get_list_or_404

from pprint import pprint

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

        # Destruindo o carrinho
        #if self.request.session.get('carrinho'):
        #    del self.request.session['carrinho']
        #    self.request.session.save()

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
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional 
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        # Trabalhando com a sessão do Django, tentando obter a chave carrinho da sessão, caso não exista criamos
        if not self.request.session.get('carrinho'):
            # Criando a chave carrinho no dicionário da sessão do usuário
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho  = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no produto " {produto_nome}". Adicionamos {variacao_estoque}x no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque
            
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario, 
                'preco_quantitativo_promocional': preco_unitario_promocional, 
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem
            }

        self.request.session.save()
        messages.success(
            self.request,
            'Produto adicionado com sucesso no carrinho'
        )

        return redirect(http_referer)

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinho')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')

class Carrinho(View):
    template_name = 'produto/carrinho.html'

    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }

        return render(self.request, self.template_name, contexto)

