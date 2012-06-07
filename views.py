# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required  

from django.conf import settings

#~ from models import Act, Invoice, Service, Price, Order, Client, Reservation

@login_required
def home(request):
    print "EXEC views.home()" # DEBUG
    #~ print request # DEBUG
    ctx = {}
    
    return render_to_response('base.html', ctx,
                            context_instance=RequestContext(request,))

