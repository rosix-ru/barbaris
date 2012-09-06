# -*- coding: utf-8 -*-
"""
###############################################################################
# Copyright 2012 Grigoriy Kramarenko.
###############################################################################
# This file is part of Barbaris.
#
#    Barbaris is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Barbaris is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Barbaris.  If not, see <http://www.gnu.org/licenses/>.
#
# Этот файл — часть Barbaris.
#
#   Barbaris - свободная программа: вы можете перераспространять ее и/или
#   изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
#   в каком она была опубликована Фондом свободного программного обеспечения;
#   либо версии 3 лицензии, либо (по вашему выбору) любой более поздней
#   версии.
#
#   Barbaris распространяется в надежде, что она будет полезной,
#   но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии ТОВАРНОГО ВИДА
#   или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной
#   общественной лицензии GNU.
#
#   Вы должны были получить копию Стандартной общественной лицензии GNU
#   вместе с этой программой. Если это не так, см.
#   <http://www.gnu.org/licenses/>.
###############################################################################
"""
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime
from django.template.defaultfilters import date as _date

register = template.Library()

@register.simple_tag
def PROJECT_NAME():
    try:
        return settings.PROJECT_NAME
    except:
        return ''

@register.simple_tag
def AUTHORS():
    try:
        return ', '.join(settings.AUTHORS)
    except:
        return ''

@register.simple_tag
def COPYRIGHT():
    try:
        return settings.COPYRIGHT
    except:
        return ''

@register.simple_tag
def COPYRIGHT_YEARS():
    end = datetime.date.today().year
    try:
        start =  settings.COPYRIGHT_YEAR
    except:
        start = datetime.date.today().year
    if start != end:
        return "%s-%s" % (start, end)
    else:
        return "%s" % end

@register.simple_tag
def navactive(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag
def subnav_filter(request, url):
    if request.get_full_path() != reverse(url):
        return """
<li>
    <a href="%s" title="Cбросить фильтр"><i class="icon-filter"></i></a>
</li>
""" % reverse(url)
    return ""

@register.simple_tag
def subnavactive(request, key, val=None):
    if val == None and (key in request.GET):
        return "active"
    if (val in ('', 0)) and (key not in request.GET):
        return "active"
    if key in request.GET:
        get_val = None
        if isinstance(val, int):
            try:
                get_val = int(request.GET.get(key))
            except:
                pass
        if isinstance(val, str):
            try:
                get_val = str(request.GET.get(key))
            except:
                pass
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
def pagination(request, paginator):
    """ paginator.paginator.count
        paginator.paginator.num_pages
        paginator.paginator.page_range
        paginator.object_list
        paginator.number
        paginator.has_next()
        paginator.has_previous()
        paginator.has_other_pages()
        paginator.next_page_number()
        paginator.previous_page_number()
        paginator.start_index()
        paginator.end_index()
    """
    temp = '<li class="%s"><a href="%s">%s</a></li>'
    number = paginator.number
    num_pages = paginator.paginator.num_pages
    DOT = '.'
    ON_EACH_SIDE = 3
    ON_ENDS = 2
    page_range = paginator.paginator.page_range
    #~ print 0, page_range
    if num_pages > 9:
        page_range = []
        if number > (ON_EACH_SIDE + ON_ENDS):
            page_range.extend(range(1, ON_EACH_SIDE))
            page_range.append(DOT)
            page_range.extend(range(number +1 - ON_EACH_SIDE, number + 1))
            #~ print 1, page_range
        else:
            page_range.extend(range(1, number + 1))
            #~ print 2, page_range
        if number < (num_pages - ON_EACH_SIDE - ON_ENDS + 1):
            page_range.extend(range(number + 1, number + ON_EACH_SIDE))
            page_range.append(DOT)
            page_range.extend(range(num_pages - ON_ENDS +1, num_pages+1))
            #~ print 3, page_range
        else:
            page_range.extend(range(number + 1, num_pages+1))
            #~ print 4, page_range
        #~ print page_range
    L = []
    for num in page_range:
        css = ""
        link = '#'
        if num == DOT:
            css = "disabled"
            num = '...'
        elif num == paginator.number:
            css = "active"
        else:
            link = addGET(request, 'page', num)
        L.append(temp % (css, link, num))
    
    return u''.join(L)

@register.simple_tag
def short_username(user):
    if not user.last_name and not user.first_name:
        return user.username
    return u'%s %s.' % (user.last_name, unicode(user.first_name)[0])

@register.simple_tag
def get_credit(order, spec=None):
    if spec:
        summa = spec.summa
    else:
        summa = 0
    debet = sum([x.debet for x in order.invoices])
    if order.invoices and debet < summa:
        credit = summa - debet
        return u'<p class="badge badge-important">Переплата: %s</p>' % credit
    
    return ''

@register.simple_tag
def integer_plus(digit1, digit2=1):
    return digit1 + digit2

@register.simple_tag
def room_button_class(room):
    return settings.BUTTON_CLASSES_STATE_ROOM[room.state]

@register.simple_tag
def room_occupied(room, order=None):
    now = datetime.datetime.now()
    sps = room.specification_set.all()
    if order:
        sps = sps.filter(order=order)
    else:
        sps = sps.filter(order__state__in=settings.SELECT_WORK_ORDERS)
        sps = sps.filter(end__gte=now).order_by('end')
    try:
        sp = sps[0]
    except:
        return u''
    return u'№%s с %s по %s' % (sp.order.id,
            _date(sp.start, "d b H:i"), 
            _date(sp.end, "d b H:i"))

def get_sp_room(room, order):
    sps = room.specification_set.all()
    sps = sps.filter(order=order)
    try:
        return sps[0]
    except:
        return None
    
@register.simple_tag
def room_start(room, order):
    sp = get_sp_room(room, order)
    if not sp:
        return u''
    return u'%s' % _date(sp.start, "Y-m-d H:i")

@register.simple_tag
def room_end(room, order):
    sp = get_sp_room(room, order)
    if not sp:
        return u''
    return u'%s' % _date(sp.end, "Y-m-d H:i")

@register.simple_tag
def room_reserved(room):
    return u'Бронь с'
