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

from django.utils.translation import ugettext_lazy as _
from django import http
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
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import date as _date
import operator
import datetime

from models import *
import forms

@login_required
def monitor(request):
    ctx = {'DEBUG': settings.DEBUG}
    ctx['object_list'] = Room.objects.all()
    ctx['settings'] = settings
    return render_to_response('monitor.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def monitor_update(request):
    ctx = {'DEBUG': settings.DEBUG}
    ctx['object_list'] = Room.objects.all()
    ctx['settings'] = settings
    return render_to_response('includes/_monitor.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
#~ def order_detail(request, pk=None, person_pk=None, action=None):
def order_detail(request, pk=None, action=None):
    print "EXEC views.order_detail()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.pk
    
    #~ if person_pk:
        #~ person = get_object_or_404(Person.objects, pk=person_pk)
    #~ else:
        #~ person = None
    
    if not pk or pk in (0, '0') or action == "new":
        order = Order(user=user)
        order_not_save = True
    else:
        order = get_object_or_404(Order, pk=pk)
        order_not_save = False
    
    def check_order():
        if order_not_save:
            #~ if person and person.pk:
                #~ order.persons.add(person.pk)
            order.save()
        return order
    
    if request.method == 'POST':
        if 'selectPerson' in request.POST:
            check_order()
            [ order.persons.add(int(x)) for x in request.POST.getlist("selectPerson", [])]
            order.save()
        elif 'deletePerson' in request.POST:
            check_order()
            [ order.persons.remove(int(x)) for x in request.POST.getlist("deletePerson", [])]
            order.save()
        
        elif 'order_comment' in request.POST:
            check_order()
            order.comment = request.POST.get('order_comment', '')
            order.save()
        
        # Specification
        elif 'specification_add' in request.POST:
            spec = Specification(order=order)
            form_spec = forms.SpecificationForm(request.POST, instance=spec)
            if form_spec.is_valid():
                spec.order = check_order()
                form_spec.save()
        elif 'specification_change' in request.POST:
            spec = Specification.objects.get(pk=request.POST.get('id',0))
            form_spec = forms.SpecificationForm(request.POST, instance=spec)
            if form_spec.is_valid():
                form_spec.save()
        elif 'specification_delete' in request.POST:
            spec = Specification.objects.get(pk=request.POST.get('id',0))
            spec.delete()
        
        # Invoice
        elif 'invoice_add' in request.POST:
            invoice = Invoice( user=user, order=check_order(), date=datetime.date.today() )
            invoice.save()
        elif 'invoice_change' in request.POST:
            invoice = Invoice.objects.get(pk=request.POST.get('id',0))
            form_invoice = forms.InvoiceForm(request.POST, instance=invoice)
            if form_invoice.is_valid():
                form_invoice.save()
        elif 'invoice_delete' in request.POST:
            invoice = Invoice.objects.get(pk=request.POST.get('id',0))
            invoice.delete()
        
        # Payment
        elif 'payment_add' in request.POST:
            invoice = Invoice.objects.get(pk=request.POST.get('id',0))
            payment = Payment( user=user, invoice=invoice, )
            payment.save()
        elif 'payment_change' in request.POST:
            payment = Payment.objects.get(pk=request.POST.get('id',0))
            form_payment = forms.PaymentForm(request.POST, instance=payment)
            if form_payment.is_valid():
                form_payment.save()
        elif 'payment_delete' in request.POST:
            payment = Payment.objects.get(pk=request.POST.get('id',0))
            payment.delete()
        
        # Акт
        elif 'act_add' in request.POST:
            act = Act( user=user, order=check_order(), date=datetime.date.today() )
            act.save()
        elif 'act_change' in request.POST:
            act = Act.objects.get(pk=request.POST.get('id',0))
            form_act = forms.ActForm(request.POST, instance=act)
            if form_act.is_valid():
                form_act.save()
        elif 'act_delete' in request.POST:
            act = Act.objects.get(pk=request.POST.get('id',0))
            act.delete()
        
        # DivDoc
        elif 'divdoc' in request.POST:
            divdoc = request.POST.get('divdoc', 0)
            order = check_order()
            if divdoc:
                order.is_divdoc = True
                order.invoice_set.all().update(summa=str(order.summa / order.persons.count()))
            else:
                order.is_divdoc = False
            order.save()
        
        if order.pk:
            return redirect("order_detail", order.pk)
    
    form_spec = forms.SpecificationForm()
    form_person = forms.PersonForm()
    form_invoice = forms.InvoiceForm()
    #~ form_invoice.fields['person'].queryset = order.persons.all()
    form_act = forms.ActForm()
    #~ form_act.fields['person'].queryset = order.persons.all()
    
    ctx['order'] = order
    ctx['settings'] = settings
    ctx['categories'] = Category.objects.all()
    ctx['reservations'] = Reservation.objects.all()
    ctx['form_spec'] = form_spec
    #~ ctx['form_person'] = form_person
    #~ ctx['form_invoice'] = form_invoice
    #~ ctx['form_act'] = form_act
    
    if order_not_save:
        return render_to_response('order_new.html', ctx,
                            context_instance=RequestContext(request,))
    return render_to_response('order_detail.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def order_accept(request):
    print "EXEC views.order_accept()" # DEBUG
    #~ print request # DEBUG
    
    if 'order_accept' in request.POST:
        order = get_object_or_404(Order.objects, pk=request.POST.get('id', 0))
        order.state = settings.STATE_ORDER_ACCEPT
        order.save()
        
        return redirect('order_detail', order.pk)
    
    return http.HttpResponseBadRequest()

@login_required
def order_cancel(request):
    print "EXEC views.order_cancel()" # DEBUG
    #~ print request # DEBUG
    
    if 'order_cancel' in request.POST:
        order = get_object_or_404(Order.objects, pk=request.POST.get('id', 0))
        order.state = settings.STATE_ORDER_CANCEL
        order.save()
        
        return redirect('order_list')
    
    return http.HttpResponseBadRequest()

@login_required
def order_dubble(request):
    print "EXEC views.order_dubble(request)" # DEBUG
    
    if 'order_dubble' in request.POST:
        order = get_object_or_404(Order.objects, pk=request.POST.get('id', 0))
        specs = order.specification_set.all()
        order.pk = None
        order.state = settings.STATE_ORDER_CREATE
        order.save()
        for spec in specs:
            spec.pk = None
            spec.order = order
            spec.save()
        
        return redirect('order_detail', order.pk)
    
    return http.HttpResponseBadRequest()

@login_required
def order_new_person(request, pk):
    print "EXEC views.order_new()" # DEBUG
    #~ print request # DEBUG
    
    if pk in ('0', 0):
        person = Person(last_name=u"Новый клиент")
        person.save()
        #~ return redirect('order_new', person.pk)
    else:
        person = get_object_or_404(Person.objects, pk=pk)
    
    return order_detail(request, None, person)

@login_required
def order_delete(request):
    print "EXEC views.order_delete()" # DEBUG
    #~ print request # DEBUG
    if 'order_delete' in request.POST:
        order = get_object_or_404(Order.objects, pk=request.POST.get('id', 0))
        order.specification_set.all().delete()
        order.delete()
    
        return redirect('order_list')
    
    return http.HttpResponseBadRequest()

@login_required
def price_list(request):
    print "EXEC views.price_list()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.pk
    ctx['categories'] = Category.objects.all()
    
    return render_to_response('price_list.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def client_list(request):
    print "EXEC views.client_list()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    session = request.session
    user = request.user
    session['user_id'] = user.pk
    
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
            #~ return http.HttpResponseBadRequest()
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
def person_detail(request, pk):
    print "EXEC views.person_detail()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    
    if pk in ('0', 0):
        person = Person(last_name=u"Новый клиент")
        detail = PersonDetail(person=person)
        person_not_save = True
    else:
        person = get_object_or_404(Person.objects, pk=pk)
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
            return http.HttpResponseRedirect(person.get_absolute_url())
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
    
    if query:
        fields = ('last_name', 'first_name', 'middle_name', 'org__title')
        persons = search(persons, fields, query)
    
    ctx['persons'] = persons[: 10]
    
    t = Template(u"""
    {% if persons %}
        <div class="controls">
        {% for person in persons %}
            <label class="checkbox">
                <input type="checkbox" name="selectPerson" value="{{ person.id }}">
                <h6>
                    {{ person }}
                    <small>{{ person.detail.birth_day|default:"" }}</small>
                </h6>
            </label>
        {% endfor %}
        </div>
        <div class="form-actions">
            <input type="submit" class="btn btn-primary" value="Добавить" />
        </div>
    {% else %}
        <h3>Персоны с такими данными не найдены</h3>
        <a target="_blank" href="{% url person_detail 0 %}">
            Добавьте персону на специальной странице.
        </a>
    {% endif %}
    """)
    
    return http.HttpResponse(t.render(Context(ctx)))

@login_required
def org_detail(request, pk):
    print "EXEC views.org_detail()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    
    if pk in ('0', 0):
        org = Org(title=u"Новая организация")
        detail = OrgDetail(org=org)
        org_not_save = True
    else:
        org = get_object_or_404(Org.objects, pk=pk)
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
            return http.HttpResponseRedirect(org.get_absolute_url())
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
def question_detail(request, pk=None, action=None):
    print "EXEC views.question_detail()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    user = request.user
    if not pk or pk in ('0', 0) or action == 'new':
        question = Question(theme=u"Новая тема вопроса")
        question.user = user
        question_not_save = True
    else:
        question = get_object_or_404(Question.objects, pk=pk)
        question_not_save = False
    
    def check_question():
        if question_not_save:
            question.save()
    
    if request.method == 'POST':
        if 'theme' in request.POST:
            form_question = forms.QuestionForm(request.POST, instance=question)
            if form_question.is_valid():
                question = form_question.save()
                return redirect('question_detail', question.pk)
        else:
            answer = Answer(user=user, question=question)
            form_answer = forms.AnswerForm(request.POST, instance=answer)
            if form_answer.is_valid():
                form_answer.save()
    
    form_question = forms.QuestionForm(instance=question)
    if not question_not_save:
        form_answer = forms.AnswerForm()
    else:
        form_answer = None
    
    ctx['question'] = question
    ctx['form_question'] = form_question
    ctx['form_answer'] = form_answer
    
    return render_to_response('question_detail.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def analyze(request):
    print "EXEC views.analyze()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    acts = Act.objects.all()
    invoices = Invoice.objects.all()
    orders = Order.objects.all()
    
    user = request.GET.get('user', '')
    if user:
        acts = acts.filter(user__pk=user)
        invoices = invoices.filter(user__pk=user)
        orders = orders.filter(user__pk=user)
    
    start = request.GET.get('start', '')
    if start:
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        acts = acts.filter(date__gte=start).filter(date__isnull=False)
        invoices = invoices.filter(date__gte=start).filter(date__isnull=False)
        orders = orders.filter(start__gte=start).filter(start__isnull=False, end__isnull=False)
        
    end = request.GET.get('end', '')
    if end:
        end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        acts = acts.filter(date__lte=end).filter(date__isnull=False)
        invoices = invoices.filter(date__lte=end).filter(date__isnull=False)
        orders = orders.filter(end__lte=end).filter(start__isnull=False, end__isnull=False)
    
    ctx['user_list'] = User.objects.filter(groups__name__in=settings.SELECT_WORK_GROUPS)
    ctx['start'] = start
    ctx['end'] = end
    
    ctx['acts'] = acts
    
    ctx['invoices']                 = invoices
    ctx['invoices_summ']            = sum([ x.summa for x in invoices ])
    ctx['invoices_payment']         = sum([ x.payment for x in invoices ])
    ctx['invoices_debet']           = sum([ x.debet for x in invoices ])
    ctx['payment_invoices']         = invoices.filter(state=settings.STATE_INVOICE_PAYMENT)
    ctx['payment_invoices_summ']    = sum([ x.summa for x in ctx['payment_invoices'] ])
    ctx['payment_invoices_payment'] = sum([ x.payment for x in ctx['payment_invoices'] ])
    ctx['payment_invoices_debet']   = sum([ x.debet for x in ctx['payment_invoices'] ])
    ctx['avance_invoices']          = invoices.filter(state=settings.STATE_INVOICE_AVANCE)
    ctx['avance_invoices_summ']     = sum([ x.summa for x in ctx['avance_invoices'] ])
    ctx['avance_invoices_payment']  = sum([ x.payment for x in ctx['avance_invoices'] ])
    ctx['avance_invoices_debet']    = sum([ x.debet for x in ctx['avance_invoices'] ])
    ctx['notpay_invoices']          = invoices.filter(state=settings.STATE_INVOICE_CREATE)
    ctx['notpay_invoices_summ']     = sum([ x.summa for x in ctx['notpay_invoices'] ])
    ctx['notpay_invoices_payment']  = sum([ x.payment for x in ctx['notpay_invoices'] ])
    ctx['notpay_invoices_debet']    = sum([ x.debet for x in ctx['notpay_invoices'] ])
    
    ctx['orders']                   = orders
    ctx['orders_summ']              = sum([ x.summa for x in ctx['orders'] ])
    ctx['orders_payment']           = sum([ x.payment for x in ctx['orders'] ])
    ctx['orders_debet']             = sum([ x.debet for x in ctx['orders'] ])
    ctx['accept_orders']            = orders.filter(state=settings.STATE_ORDER_ACCEPT)
    ctx['accept_orders_summ']       = sum([ x.summa for x in ctx['accept_orders'] ])
    ctx['accept_orders_payment']    = sum([ x.payment for x in ctx['accept_orders'] ])
    ctx['accept_orders_debet']      = sum([ x.debet for x in ctx['accept_orders'] ])
    ctx['close_orders']             = orders.filter(state=settings.STATE_ORDER_CLOSE)
    ctx['close_orders_summ']        = sum([ x.summa for x in ctx['close_orders'] ])
    ctx['close_orders_payment']     = sum([ x.payment for x in ctx['close_orders'] ])
    ctx['close_orders_debet']       = sum([ x.debet for x in ctx['close_orders'] ])
    ctx['cancel_orders']            = orders.filter(state=settings.STATE_ORDER_CANCEL)
    ctx['cancel_orders_summ']       = sum([ x.summa for x in ctx['cancel_orders'] ])
    ctx['cancel_orders_payment']    = sum([ x.payment for x in ctx['cancel_orders'] ])
    ctx['cancel_orders_debet']      = sum([ x.debet for x in ctx['cancel_orders'] ])
    
    return render_to_response('analyze.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def object_list(request, model, template_name, search_fields=[],
    date_field="", use_stats=False, foreign_field="", foreign_key="",
    use_distinct=False,
    ):
    print "EXEC views.object_list(...)" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    page = 1
    qs = model.objects.all()
    
    if foreign_field and foreign_key:
        qs = qs.filter(Q(**{ foreign_field + "__exact": foreign_key }))
    
    if date_field:
        
        ctx['years']  = [ x.year  for x in qs.dates(date_field, 'year') ]
        ctx['months'] = [ x.month for x in qs.dates(date_field, 'month') ]
        ctx['days']   = [ x.day   for x in qs.dates(date_field, 'day') ]
        
        for key in ('year','month', 'day'):
            val = request.GET.get(key, "")
            if val:
                qs = qs.filter(Q(**{ date_field + "__" + key: val }))
        
        date_start = request.GET.get("date_start", "")
        if date_start:
            qs = qs.filter(Q(**{ date_field + "__gte": date_start }))
        
        date_end = request.GET.get("date_end", "")
        if date_end:
            qs = qs.filter(Q(**{ date_field + "__lte": date_end }))
    
    if use_stats:
        ctx['stats'] = eval("settings.STATE_%s_CHOICES" % model.__name__.upper())
        
        state = request.GET.get("state", "")
        if state:
            qs = qs.filter(state=state)
    
    if use_distinct:
            qs = qs.distinct()
    
    if 'q' in request.GET:
        qs = search(qs,search_fields, request.GET.get('q', ""))
        ctx['q'] = request.GET.get('q', "")
    if 'query' in request.GET:
        qs = search(qs,search_fields, request.GET.get('query', ""))
        ctx['query'] = request.GET.get('query', "")
    if 'page' in request.GET:
        page = request.GET.get('page', 1)
    ctx['paginator'] = get_paginator(qs, page)
    
    return render_to_response(template_name, ctx,
                            context_instance=RequestContext(request,))

@login_required
def object_detail(request, model, template_name, pk):
    print "EXEC views.object_detail(...)" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    ctx['object'] = get_object_or_404(model.objects, pk=pk)
    return render_to_response(template_name, ctx,
                            context_instance=RequestContext(request,))

@login_required
def document_print(request, pk, model, document):
    print "EXEC views.document_print(...)" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    
    doc = get_object_or_404(model, pk=pk)
    
    if 'form' in request.GET:
        temp = get_object_or_404(DocTemplate, document=document, pk=request.GET.get('form',0))
    else:
        temp = get_object_or_404(DocTemplate, document=document, is_default=True)
    
    ctx['document'] = doc
    ctx['supplier'] = Org.sellers.all()[0]
    ctx['STATIC_URL'] = settings.STATIC_URL
    ctx['template_list'] = DocTemplate.objects.filter(document=document)
    if temp.fname:
        t = get_template(temp.fname)
    else:
        t = Template(temp.text)
    ctx['template'] = temp
    ctx['document_body'] = t.render(Context(ctx))
    return render_to_response('document_print.html', ctx,
                            context_instance=RequestContext(request,))

@login_required
def get_modal(request, obj, key, pk):
    print "EXEC views.get_modal()" # DEBUG
    #~ print request # DEBUG
    ctx = {'DEBUG': settings.DEBUG}
    #~ if not request.is_ajax():
        #~ return http.HttpResponseBadRequest
    session = request.session
    user = request.user
    session['user_id'] = user.pk
    
    #~ try:
    Class = eval(obj.title())
    instance = get_object_or_404(Class, pk=pk)
    Form = eval('forms.'+obj.title()+'Form')
    form = Form(instance = instance)
    
    ctx['object'] = instance
    ctx['form'] = form
    #~ except:
        #~ return http.HttpResponseBadRequest()
    template = 'modals/_modal_%s_%s.html' % (obj.lower(), key.lower())
    
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
            try:
                print unicode(queryset.query)
            except:
                pass
        
    return queryset

def get_paginator(qs, page=1, on_page=50):
    paginator = Paginator(qs, on_page)
    try:
        page_qs = paginator.page(int(page))
    except (EmptyPage, InvalidPage):
        page_qs = paginator.page(paginator.num_pages)
    #~ print 'get_paginator:',page, 'from', page_qs.paginator.num_pages
    return page_qs
