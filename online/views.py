# -*- coding: utf-8 -*-
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
    
    
    return render_to_response('monitor.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def orders(request):
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
def pricelist(request):
    print "EXEC views.pricelist()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
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
    
    return render_to_response('clients.html', ctx,
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
