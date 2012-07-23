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

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson  
from django.contrib.auth.decorators import login_required  
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.cache import cache
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.defaultfilters import date as _date
import operator
import datetime

from barbaris.online.models import *

@login_required
def monitor(request):
    print "EXEC views.monitor()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    now = datetime.datetime.now()
    ctx['current_month'] = _date(now, 'F')
    ctx['next_month'] = _date(datetime.datetime(now.year, now.month +1, 1), 'F')
    
    categories = Category.objects.all()
    hotel = categories.get(title="Hotel")
    ctx['hotel_services'] = hotel.service_set.all()
    sauna = categories.get(title="Sauna")
    
    rooms = Room.objects.all()
    
    sps = Specification.objects.all()
    
    # Занятые комнаты: освободились на текущий момент,
    # занимаются позднее чем завтра.
    sps_rooms = sps.filter(room__isnull=False,
            end__gt=now,
            start__lt=now.date() + datetime.timedelta(1)
            )
    room_ids = [ x.room.id for x in sps_rooms ]
    ctx['sps_rooms_nonfree'] = rooms.filter(id__in=sps_rooms)
    ctx['rooms_free'] = rooms.exclude(id__in=room_ids)
    
    # Бронирование комнат
    sps_room_reserv = sps.filter(room__isnull=False,
            reservation__isnull=False,
            end__gt=now,
            start__gte=now.date()
            )
    # На сегодня
    ctx['sps_rooms_reserv_today'] = sps_room_reserv.filter(
            start__lt=now.date() + datetime.timedelta(1)
            )
    # На завтра
    ctx['sps_rooms_reserv_tomorrow'] = sps_room_reserv.filter(
            start__range=(now.date(), now.date() + datetime.timedelta(2))
            )
    
    
    
    return render_to_response('monitor.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def orders(request, key=None, id=None):
    print "EXEC views.orders()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    orders = Order.objects.all()
    
    if request.GET:
        try:
            state = int(request.GET.get('state', 0))
            year = int(request.GET.get('year', 0))
            month = int(request.GET.get('month', 0))
            day = int(request.GET.get('day', 0))
            query = request.GET.get('query', '')
        except:
            return HttpResponseBadRequest(u'Неверные параметры запроса')
        if state:
            orders = orders.filter(state=state)
        if year:
            orders = orders.filter(updated__year=year)
        if month:
            orders = orders.filter(updated__month=month)
        if day:
            orders = orders.filter(updated__day=day)
        if query:
            search_fields = (
                'client__last_name',
                'client__first_name',
                'client__middle_name',
            )
            orders = search(orders, search_fields, query)
        ctx['query'] = query
    
    ctx['orders'] = orders
    ctx['years']  = [ x.year  for x in orders.dates('updated', 'year') ]
    ctx['months'] = [ x.month for x in orders.dates('updated', 'month') ]
    ctx['days']   = [ x.day   for x in orders.dates('updated', 'day') ]
    ctx['stats']   = settings.STATE_ORDER_CHOICES
    
    return render_to_response('orders.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def new_order(request, key, id):
    print "EXEC views.orders()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('new_order.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def pricelist(request):
    print "EXEC views.pricelist()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    ctx['categories'] = Category.objects.all()
    
    return render_to_response('pricelist.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def invoices(request):
    print "EXEC views.invoices()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('invoices.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def acts(request):
    print "EXEC views.acts()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('acts.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def clients(request):
    print "EXEC views.clients()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    # Организации
    organizations = Organization.buyers.all()
    # Люди
    clients = Client.objects.all()
    
    page_cli = 1
    page_org = 1
    show_orgs = 1
    show_clients = 1
    query = ''
    
    if request.GET:
        try:
            page_cli = int(request.GET.get('page_cli'))
        except:
            page_cli = 1
        try:
            page_org = int(request.GET.get('page_org'))
        except:
            page_org = 1
        show_orgs = request.GET.get('show_orgs', 1)
        show_clients = request.GET.get('show_clients', 1)
        #~ if show_orgs and show_clients and page > 1:
            #~ return HttpResponseBadRequest()
        query = request.GET.get('query', '')
    
        if query:
            #~ if show_orgs and not show_clients:
                #~ fields = ('title',)
                #~ organizations = search(organizations, fields, query)
            #~ elif show_clients:
                #~ fields = ('last_name', 'first_name', 'middle_name')
                #~ clients = search(clients, fields, query)
            #~ else:
                fields = ('title',)
                organizations = search(organizations, fields, query)
                fields = ('last_name', 'first_name', 'middle_name')
                clients = search(clients, fields, query)
    
    
    if show_clients:
        ctx['clients'] = get_paginator(clients, page_cli)
    else:
        ctx['clients'] = ctx['pagination_list_clients'] = []
    
    if show_orgs:
        ctx['organizations'] = get_paginator(organizations, page_org, 10)
    else:
        ctx['organizations'] = ctx['pagination_list_orgs'] = []
    
    ctx['query'] = query
    return render_to_response('clients.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def client_detail(request, id):
    print "EXEC views.clients()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('client_detail.html', ctx,
                            context_instance=RequestContext(request,))


@login_required
def org_detail(request, id):
    print "EXEC views.clients()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('org_detail.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def analyze(request):
    print "EXEC views.analyze()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('analyze.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def reports(request):
    print "EXEC views.reports()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('reports.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def questions(request):
    print "EXEC views.questions()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('questions.html', ctx,
                            context_instance=RequestContext(request,))

########################################################################
# Вспомогательные функции
########################################################################
def search(queryset, search_fields, query):
    """ Фильтрация """
    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name
    orm_lookups = [construct_search(str(search_field))
                   for search_field in search_fields]
    for bit in query.split():
        or_queries = [Q(**{orm_lookup: bit})
                      for orm_lookup in orm_lookups]
        queryset = queryset.filter(reduce(operator.or_, or_queries))
    
    return queryset

def get_paginator(qs, page=1, on_page=25):
    paginator = Paginator(qs, on_page)
    try:
        page_qs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_qs = paginator.page(paginator.num_pages)
    
    return page_qs
