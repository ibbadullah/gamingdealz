from django import template
from decimal import Decimal


register = template.Library()


@register.filter(name='totalOffset')
def total_offset(val1):
    if val1.get('estimated_total', None) > val1.get('offset', None):
        return True
    return False


@register.filter(name='back')
def back(val1):
    return round(val1 - 20)


@register.filter(name='next')
def next(val1):
    return round(val1 + 20)


@register.filter(name='priceDot')
def priceDot(val1):
    convertF = Decimal(val1)
    rounding = round(convertF,2)
    return str(rounding).replace('.', ',')
