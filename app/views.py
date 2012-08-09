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
from django.template import RequestContext, Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404, redirect
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

from models import *
import forms

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
    ctx['hotel_services'] = hotel.service_set.filter(is_rooms=True)
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
    ctx['sps_rooms_nonfree'] = sps_rooms
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
def order_list(request, key=None, id=None):
    print "EXEC views.order_list()" # DEBUG
    print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    orders = Order.objects.all()
    
    person, org = (None, None)
    
    if key == 'person':
        person = get_object_or_404(Person.objects, id=id)
        person_not_save = False
        orders = orders.filter(person=person)
    
    elif key == 'org':
        org = get_object_or_404(Org.objects, id=id)
        org_not_save = False
        orders = orders.filter(person__org=org)
    
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
                'person__last_name',
                'person__first_name',
                'person__middle_name',
            )
            orders = search(orders, search_fields, query)
        ctx['query'] = query
    
    ctx['person'] = person
    ctx['org'] = org
    ctx['orders'] = orders
    ctx['years']  = [ x.year  for x in orders.dates('updated', 'year') ]
    ctx['months'] = [ x.month for x in orders.dates('updated', 'month') ]
    ctx['days']   = [ x.day   for x in orders.dates('updated', 'day') ]
    ctx['stats']   = settings.STATE_ORDER_CHOICES
    
    return render_to_response('order_list.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def order_detail(request, id=None, person=None):
    print "EXEC views.order_detail()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    if not id or id in (0, '0'):
        order = Order(user=user)
        order.person = person
        order_not_save = True
    else:
        order = get_object_or_404(Order, id=id)
        order_not_save = False
    
    def check_order():
        if order_not_save:
            order.save()
        return order
    
    if request.method == 'POST':
        if 'specification_delete' in request.POST:
            try:
                id = request.POST['specification_delete']
                Specification.objects.filter(id=id).all().delete()
            except:
                pass
        elif 'specification' in request.POST:
            spec = Specification(order=order)
            form_spec = forms.SpecificationForm(request.POST, instance=spec)
            if form_spec.is_valid():
                spec.order = check_order()
                form_spec.save()
        elif 'select_person' in request.POST:
            order.person = get_object_or_404(Person, id=request.POST.get("selectPerson", None))
            order.save()
        elif 'select_other_persons' in request.POST:
            [ order.other_persons.add(int(x)) for x in request.POST.getlist("selectPerson", [])]
            order.save()
        elif 'deletePerson' in request.POST:
            [ order.other_persons.remove(int(x)) for x in request.POST.getlist("deletePerson", [])]
            order.save()
        elif 'invoice_add' in request.POST:
            invoice = Invoice( user=user, order=check_order(), date=datetime.date.today() )
            invoice.save()
        elif 'invoice_delete' in request.POST:
            try:
                id = request.POST['invoice_delete']
                print id
                Invoice.objects.filter(id=id).all().delete()
            except:
                pass
        elif 'invoice_change' in request.POST:
            invoice = Invoice.objects.get(id=request.POST.get('id',0))
            form_invoice = forms.InvoiceForm(request.POST, instance=invoice)
            if form_invoice.is_valid():
                form_invoice.save()
        elif 'act_add' in request.POST:
            invoice = Act( user=user, order=check_order(), date=datetime.date.today() )
            invoice.save()
        elif 'act_delete' in request.POST:
            try:
                id = request.POST['invoice_delete']
                Invoice.objects.filter(id=id).all().delete()
            except:
                pass
        
        
        if order.id:
            return redirect("order_detail", order.id)
    
    form_spec = forms.SpecificationForm()
    form_person = forms.PersonForm(instance=order.person)
    form_invoice = forms.InvoiceForm()
    form_act = forms.ActForm()
    
    ctx['order'] = order
    ctx['settings'] = settings
    ctx['person'] = order.person
    ctx['categories'] = Category.objects.all()
    ctx['reservations'] = Reservation.objects.all()
    ctx['form_spec'] = form_spec
    ctx['form_person'] = form_person
    ctx['form_invoice'] = form_invoice
    ctx['form_act'] = form_act
    
    if order_not_save:
        return render_to_response('order_new.html', ctx,
                            context_instance=RequestContext(request,))
    return render_to_response('order_detail.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def order_action(request, id, key):
    print "EXEC views.order_action()" # DEBUG
    #~ print request # DEBUG
    
    order = get_object_or_404(Order.objects, id=id)
    if key == 'reserv' and order.state_create:
        order.state = settings.STATE_ORDER_RESERV
        order.save()
    if key == 'accept' and ( order.state_create or order.state_reserv ):
        order.state = settings.STATE_ORDER_ACCEPT
        order.save()
    
    
    return redirect('order_detail', order.id)

@login_required
def order_new_person(request, id):
    print "EXEC views.order_new()" # DEBUG
    #~ print request # DEBUG
    
    if id in ('0', 0):
        person = Person(last_name="Новый клиент")
        person.save()
        #~ return redirect('order_new', person.id)
    else:
        person = get_object_or_404(Person.objects, id=id)
    
    return order_detail(request, None, person)

@login_required
def order_delete(request, id):
    print "EXEC views.order_delete()" # DEBUG
    #~ print request # DEBUG
    
    order = get_object_or_404(Order.objects, id=id, state=1)
    order.specification_set.all().delete()
    order.delete()
    
    return redirect('order_list')

@login_required
def specification_delete(request, id):
    print "EXEC views.order_new()" # DEBUG
    #~ print request # DEBUG
    
    sp = get_object_or_404(Specification.objects, id=id)
    sp.delete()
    
    return  HttpResponseRedirect()

@login_required
def price_list(request):
    print "EXEC views.price_list()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    ctx['categories'] = Category.objects.all()
    
    return render_to_response('price_list.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def invoice_list(request, id=None):
    print "EXEC views.invoice_list()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    invoices = Invoice.objects.all()
    ctx['invoice_list'] = invoices
    
    return render_to_response('invoice_list.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def invoice_detail(request, id, add=None):
    print "EXEC views.invoice_detail()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    
    return render_to_response('invoice_detail.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def act_list(request):
    print "EXEC views.act_list()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    acts = Act.objects.all()
    ctx['act_list'] = acts
    
    return render_to_response('act_list.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def act_detail(request, id):
    print "EXEC views.act_order()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    
    return render_to_response('act_detail.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def client_list(request):
    print "EXEC views.client_list()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    # Организации
    orgs = Org.buyers.all()
    # Люди
    persons = Person.objects.all()
    
    page_persons = 1
    page_orgs = 1
    show_orgs = 1
    show_persons = 1
    query = ''
    
    if request.GET:
        try:
            page_persons = int(request.GET.get('page_persons'))
        except:
            page_persons = 1
        try:
            page_orgs = int(request.GET.get('page_orgs'))
        except:
            page_orgs = 1
        show_orgs = request.GET.get('show_orgs', 1)
        show_persons = request.GET.get('show_persons', 1)
        #~ if show_orgs and show_persons and page > 1:
            #~ return HttpResponseBadRequest()
        query = request.GET.get('query', '')
    
        if query:
            #~ if show_orgs and not show_persons:
                #~ fields = ('title',)
                #~ orgs = search(orgs, fields, query)
            #~ elif show_persons:
                #~ fields = ('last_name', 'first_name', 'middle_name')
                #~ persons = search(persons, fields, query)
            #~ else:
                fields = ('title',)
                orgs = search(orgs, fields, query)
                fields = ('last_name', 'first_name', 'middle_name', 'org__title')
                persons = search(persons, fields, query)
    
    
    if show_persons:
        ctx['persons'] = get_paginator(persons, page_persons)
    else:
        ctx['persons'] = ctx['pagination_list_persons'] = []
    
    if show_orgs:
        ctx['orgs'] = get_paginator(orgs, page_orgs, 10)
    else:
        ctx['orgs'] = ctx['pagination_list_orgs'] = []
    
    ctx['query'] = query
    return render_to_response('client_list.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def person_detail(request, id):
    print "EXEC views.person_detail()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    
    if id in ('0', 0):
        person = Person(last_name="Новый клиент")
        detail = PersonDetail(person=person)
        person_not_save = True
    else:
        person = get_object_or_404(Person.objects, id=id)
        detail = person.detail
        person_not_save = False
    
    def check_person():
        if person_not_save:
            person.save()
            detail.person = person
            form_person = forms.PersonForm(instance=person)
            if form_person.is_valid():
                form_person.save()
    
    if request.method == 'POST':
        if 'last_name' in request.POST:
            form_person = forms.PersonForm(request.POST, instance=person)
            if form_person.is_valid():
                form_person.save()
        else:
            form_person = forms.PersonForm(instance=person)
        if 'document_type' in request.POST:
            form_document = forms.PersonDocumentForm(request.POST, instance=detail)
            check_person()
            if form_document.is_valid():
                form_document.save()
        else:
            form_document = forms.PersonDocumentForm(instance=detail)
        if 'birth_day' in request.POST:
            form_birth = forms.PersonBirthForm(request.POST, instance=detail)
            check_person()
            if form_birth.is_valid():
                form_birth.save()
        else:
            form_birth = forms.PersonBirthForm(instance=detail)
        
        if 'residence_country' in request.POST:
            form_residence = forms.PersonResidenceForm(request.POST, instance=detail)
            check_person()
            if form_residence.is_valid():
                form_residence.save()
        else:
            form_residence = forms.PersonResidenceForm(instance=detail)
        if person_not_save:
            return HttpResponseRedirect(person.get_absolute_url())
    else:
        form_person = forms.PersonForm(instance=person)
        form_document = forms.PersonDocumentForm(instance=detail)
        form_birth = forms.PersonBirthForm(instance=detail)
        form_residence = forms.PersonResidenceForm(instance=detail)
    
    ctx['person'] = person
    ctx['form_person'] = form_person
    ctx['form_document'] = form_document
    ctx['form_birth'] = form_birth
    ctx['form_residence'] = form_residence
    
    return render_to_response('person_detail.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def person_search(request):
    print "EXEC views.org_detail()" # DEBUG
    #~ print request # DEBUG
    ctx = { 'DEBUG': settings.DEBUG }
    persons = Person.objects.all()
    
    query = request.GET.get('query', '')
    destination = request.GET.get('destination', 'default')
    
    hidden_names = {'default':'select_person', 
            'person':'select_person', 
            'other_persons':'select_other_persons' 
        }
    ctx['hidden_name'] = hidden_names[destination]
    
    input_types = {'default':'radio', 'person':'radio', 'other_persons':'checkbox' }
    ctx['input_type'] = input_types[destination]
    
    if query:
        fields = ('last_name', 'first_name', 'middle_name', 'org__title')
        persons = search(persons, fields, query)
    
    ctx['persons'] = persons[: 10]
    
    t = Template("""
    {% if persons %}
        <div class="controls">
        {% for person in persons %}
            <label class="{{ input_type }}">
                <input type="{{ input_type }}" name="selectPerson" value="{{ person.id }}">
                <h6>
                    {{ person }}
                    <small>{{ person.detail.birth_day|default:"" }}</small>
                </h6>
            </label>
        {% endfor %}
        </div>
        <div class="form-actions">
            <input type="hidden" name="{{ hidden_name }}" value="true" />
            <input type="submit" class="btn btn-primary" value="Установить" />
        </div>
    {% else %}
        <h3>Персоны с такими данными не найдены</h3>
        <a target="_blank" href="{% url person_detail 0 %}">
            Добавьте персону на специальной странице.
        </a>
    {% endif %}
    """)
    
    return HttpResponse(t.render(Context(ctx)))

@login_required
def org_detail(request, id):
    print "EXEC views.org_detail()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    
    if id in ('0', 0):
        org = Org(title="Новая организация")
        detail = OrgDetail(org=org)
        org_not_save = True
    else:
        org = get_object_or_404(Org.objects, id=id)
        detail = org.detail
        org_not_save = False
    
    def check_org():
        if org_not_save:
            org.save()
            detail.org = org
            form_org = forms.OrgForm(instance=org)
            if form_org.is_valid():
                form_org.save()
    
    if request.method == 'POST':
        if 'title' in request.POST:
            form_org = forms.OrgForm(request.POST, instance=org)
            if form_org.is_valid():
                form_org.save()
        else:
            form_org = forms.OrgForm(instance=org)
        
        if 'fulltitle' in request.POST:
            form_detail = forms.OrgDetailForm(request.POST, instance=detail)
            check_org()
            if form_detail.is_valid():
                form_detail.save()
        else:
            form_detail = forms.OrgDetailForm(instance=detail)
        
        if 'document_type' in request.POST:
            form_document = forms.OrgDocumentForm(request.POST, instance=detail)
            check_org()
            if form_document.is_valid():
                form_document.save()
        else:
            form_document = forms.OrgDocumentForm(instance=detail)
        
        if 'bank_bik' in request.POST:
            form_bank = forms.OrgBankForm(request.POST, instance=detail)
            check_org()
            if form_bank.is_valid():
                form_bank.save()
        else:
            form_bank = forms.OrgBankForm(instance=detail)
        
        if org_not_save:
            return HttpResponseRedirect(org.get_absolute_url())
    else:
        form_org = forms.OrgForm(instance=org)
        form_detail = forms.OrgDetailForm(instance=detail)
        form_document = forms.OrgDocumentForm(instance=detail)
        form_bank = forms.OrgBankForm(instance=detail)
    
    ctx['org'] = org
    ctx['form_org'] = form_org
    ctx['form_detail'] = form_detail
    ctx['form_document'] = form_document
    ctx['form_bank'] = form_bank
    
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
def report_list(request):
    print "EXEC views.report_list()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('report_list.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def document_print(request, key, id):
    print "EXEC views.document_print(request, key, id)" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    
    try:
        doc = get_object_or_404(eval(key.title()), id=id)
    except:
        return HttpResponseBadRequest()
    
    if 'form' in request.GET:
        temp = get_object_or_404(DocTemplate, document=key, id=request.GET.get('form',0))
    else:
        temp = get_object_or_404(DocTemplate, document=key, is_default=True)
    
    ctx['document'] = doc
    ctx['seller'] = Org.sellers.all()[0]
    ctx['static_url'] = settings.STATIC_URL
    ctx['template_list'] = DocTemplate.objects.filter(document=key)
    if temp.fname:
        t = get_template(temp.fname)
    else:
        t = Template(temp.text)
    ctx['template'] = temp
    ctx['document_body'] = t.render(Context(ctx))
    return render_to_response('document_print.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def question_list(request):
    print "EXEC views.question_list()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    return render_to_response('question_list.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def get_modal(request, obj, key, id):
    print "EXEC views.get_modal()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    #~ if not request.is_ajax():
        #~ return HttpResponseBadRequest
    session = request.session
    user = request.user
    session['user_id'] = user.id
    
    #~ try:
    Class = eval(obj.title())
    instance = get_object_or_404(Class, id=id)
    Form = eval('forms.'+obj.title()+'Form')
    form = Form(instance = instance)
    
    ctx['object'] = instance
    ctx['form'] = form
    #~ except:
        #~ return HttpResponseBadRequest()
    template = 'modals/_modal_%s_%s.html' % (obj.lower(), key.lower())
    print template
    return render_to_response(
            template, ctx, context_instance=RequestContext(request,))

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
    
    if settings.DEBUG:
        try:
            print queryset.query
        except:
            print unicode(queryset.query)
        
    return queryset

def get_paginator(qs, page=1, on_page=25):
    paginator = Paginator(qs, on_page)
    try:
        page_qs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_qs = paginator.page(paginator.num_pages)
    
    return page_qs
