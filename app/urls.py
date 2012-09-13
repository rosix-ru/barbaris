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

from django.conf.urls.defaults import patterns, url
from project.app.models import *

PERSON_LIST = { 'model': Person, 'template_name': "person_list.html", 
        'search_fields': [
            'last_name', 
            'first_name',
            'middle_name',
            'org__title',
            ]
        }
PERSON_PRINT = { 'model': Person, 'document': 'person', }

ORG_LIST = { 'model': Org, 'template_name': "org_list.html", 
        'search_fields': [
            'title',
            ]
        }
ORG_PRINT = { 'model': Org, 'document': 'org', }

PRICE_LIST = { 'model': Category, 'template_name': "price_list.html", 
        'search_fields': [
            'service__title',
            'service__category__title',
            ],
        }
PRICE_PRINT = { 'model': Price, 'template_name': "price_list.html", 'document': 'price', }

ORDER_LIST = { 'model': Order, 'template_name': "order_list.html", 
        'search_fields': [
            'id',
            'persons__last_name', 
            'persons__first_name',
            'persons__middle_name',
            'persons__org__title',
            ],
        'date_field': 'created', 'use_stats': True,
        'use_distinct': True,
        }

ORDER_LIST_CLIENT = ORDER_LIST.copy()
ORDER_LIST_CLIENT.update({ 'foreign_field': "clients__id", })
#~ ORDER_LIST_PERSON = ORDER_LIST.copy()
#~ ORDER_LIST_PERSON.update({ 'foreign_field': "persons__id", })
#~ ORDER_LIST_ORG = ORDER_LIST.copy()
#~ ORDER_LIST_ORG.update({ 'foreign_field': "persons__org__id", })


INVOICE_LIST = { 'model': Invoice, 'template_name': "invoice_list.html", 
        'search_fields': [
            'id',
            'order__persons__last_name', 
            'order__persons__first_name',
            'order__persons__middle_name',
            'order__persons__org__title',
            ],
        'date_field': 'date', 'use_stats': True,
        }
INVOICE_PRINT = { 'model': Invoice, 'document': 'invoice', }

ACT_LIST = { 'model': Act, 'template_name': "act_list.html", 
        'search_fields': [
            'id',
            'order__persons__last_name', 
            'order__persons__first_name',
            'order__persons__middle_name',
            'order__persons__org__title',
            ],
        'date_field': 'date',
        }
ACT_PRINT = { 'model': Act, 'document': 'act', }

QUESTION_LIST = { 'model': Question, 'template_name': "question_list.html", 
        'search_fields': [
            'text', 
            'user__last_name',
            'user__first_name',
            'user__username',
            ],
        'date_field': 'created',
        }

PERSON_DETAIL = { "model" : Person, "template_name" : "person_detail.html" }
ORG_DETAIL = { "model" : Org, "template_name" : "org_detail.html" }

urlpatterns = patterns('project.app.views',
    url(r'^$',                          'monitor',              name='monitor'),
    url(r'^monitor/update/$',           'monitor_update',       name='monitor_update'),
    url(r'^analyze/$',                  'analyze',              name='analyze'),
    
    url(r'^persons/$',    'object_list',      name='person_list',     kwargs = PERSON_LIST),
    url(r'^orgs/$',       'object_list',      name='org_list',        kwargs = ORG_LIST),
    url(r'^prices/$',     'object_list',      name='price_list',      kwargs = PRICE_LIST),
    url(r'^invoices/$',   'object_list',      name='invoice_list',    kwargs = INVOICE_LIST),
    url(r'^acts/$',       'object_list',      name='act_list',        kwargs = ACT_LIST),
    url(r'^questions/$',  'object_list',      name='question_list',   kwargs = QUESTION_LIST),
    url(r'^orders/$',     'object_list',      name='order_list',      kwargs = ORDER_LIST),
    url(r'^orders/client(?P<foreign_key>\d+)/$',     
                                            'object_list',      name='client_orders',   kwargs = ORDER_LIST_CLIENT),
    #~ url(r'^orders/person(?P<foreign_key>\d+)/$',     
                                            #~ 'object_list',      name='person_orders',   kwargs = ORDER_LIST_PERSON),
    #~ url(r'^orders/org(?P<foreign_key>\d+)/$',     
                                            #~ 'object_list',      name='org_orders',      kwargs = ORDER_LIST_ORG),
    
    
    url(r'^client/(?P<pk>\d+)/$',           'client_detail',    name='client_detail'),
    url(r'^person/(?P<pk>\d+)/$',           'person_detail',    name='person_detail'),
    #~ url(r'^person/(?P<person_pk>\d+)/order/new/$', 
                                            #~ 'order_detail',     name='person_new_order',    kwargs = {'action': 'new'}),
    #~ url(r'^person/search/$',                'person_search',    name='person_search'),
    url(r'^client/search/$',                'client_search',    name='client_search'),
    url(r'^client/new/$',                   'client_create',    name='client_create'),
    
    url(r'^org/(?P<pk>\d+)/$',              'org_detail',       name='org_detail'),
    
    url(r'^order/(?P<pk>\d+)/$',       'order_detail',         name='order_detail'),
    url(r'^order/new/$',               'order_detail',         name='order_new',            kwargs = {'action': 'new'}),
    url(r'^order/dubble/$',            'order_dubble',         name='order_dubble'),
    url(r'^order/delete/$',            'order_delete',         name='order_delete'),
    url(r'^order/accept/$',            'order_accept',         name='order_accept'),
    url(r'^order/cancel/$',            'order_cancel',         name='order_cancel'),
    url(r'^specifications/info/$',     'sp_info',              name='sp_info'),
    
    url(r'^print/invoice/(?P<pk>\d+)/$',    'document_print',       name='invoice_print',   kwargs = INVOICE_PRINT),
    url(r'^print/act/(?P<pk>\d+)/$',        'document_print',       name='act_print',       kwargs = ACT_PRINT),
    url(r'^print/person/(?P<pk>\d+)/$',     'document_print',       name='person_print',    kwargs = PERSON_PRINT),
    url(r'^print/org/(?P<pk>\d+)/$',        'document_print',       name='org_print',       kwargs = ORG_PRINT),
    
    url(r'^question/(?P<pk>\d+)/$',     'question_detail',      name='question_detail', ),
    url(r'^question/new/$',             'question_detail',      name='question_new',            kwargs = {'action': 'new'}),
    
    url(r'^modal/(?P<obj>\w+)/(?P<key>\w+)/(?P<pk>\d+)/$',
                                        'get_modal',            name='get_modal'),
)
