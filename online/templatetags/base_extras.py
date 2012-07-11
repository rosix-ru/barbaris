from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag
def addGET(request, key, val=''):
    dic = request.GET.copy()
    dic[key] = val
    L = ['%s=%s' % (k, v) for k,v in dic.items()] 
    return "?" + '&'.join(L)
