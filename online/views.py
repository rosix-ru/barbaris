# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
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


