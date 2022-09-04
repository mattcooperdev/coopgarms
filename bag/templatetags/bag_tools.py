from django import template

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    ''' Update subtotal in bag '''
    return price * quantity
