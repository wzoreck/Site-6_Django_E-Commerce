from django.template import Library

register = Library()

@register.filter
def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')

@register.filter
def quantidade_total_carrinho(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

@register.filter
def preco_total_carrinho(carrinho):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item
            in carrinho.values()
        ]
    )
