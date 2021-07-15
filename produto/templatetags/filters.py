from django.template import Library

register = Library()

@register.filter
def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')

@register.filter
def quantidade_total_carrinho(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])