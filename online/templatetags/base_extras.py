from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag
def subnavactive(request, key, val=None):
    if val == None and (key in request.GET):
        return "active"
    if (val in ('', 0)) and (key not in request.GET):
        return "active"
    if key in request.GET:
        if isinstance(val, int):
            try:
                get_val = int(request.GET.get(key))
            except:
                get_val = None
        if isinstance(val, str):
            try:
                get_val = str(request.GET.get(key))
            except:
                get_val = None
        if get_val == val:
                return "active"
    return ""

@register.simple_tag
def addGET(request, key, val=''):
    dic = request.GET.copy()
    if val:
        dic[key] = val
    else:
        try:
            del dic[key]
        except:
            pass
    L = ['%s=%s' % (k, v) for k,v in dic.items()] 
    return "?" + '&'.join(L)

@register.simple_tag
def short_username(user):
    if not user.last_name and not user.first_name:
        return user.username
    return u'%s %s.' % (user.last_name, unicode(user.first_name)[0])
