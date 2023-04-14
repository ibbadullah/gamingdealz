from django import template
from adminpanel.models import Favourite

register = template.Library()


@register.filter(name='checkId')
def checkId(id):
    if Favourite.objects.filter(offer_id=id).exists():
        return True
    return False


@register.filter(name='nextPage')
def nextPage(offset):
    return int(offset) + 20


@register.filter(name='prevPage')
def prevPage(offset):
    return int(offset) - 20


@register.filter(name='intToFloat')
def convertIntToFloat(value):
    return format(float(value), ".2f").replace('.', ',')
