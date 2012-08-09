# -*- coding: utf-8 -*-
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

from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from datetime import date

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
    end = date.today().year
    try:
        start =  settings.COPYRIGHT_YEAR
    except:
        start = date.today().year
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
