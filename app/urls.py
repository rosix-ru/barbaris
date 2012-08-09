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

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('project.app.views',
    url(r'^$',                          'monitor',              name='monitor'),
    
    url(r'^orders/$',                   'order_list',           name='order_list'),
    url(r'^orders/(\d+)/$',             'order_detail',         name='order_detail'),
    url(r'^orders/new/$',               'order_detail',         name='order_new'),
    url(r'^orders/new/(\d+)/$',         'order_new_person',     name='order_new_person'),
    url(r'^orders/delete/(\d+)/$',      'order_delete',         name='order_delete'),
    url(r'^orders/(\d+)/action/(\w+)/$','order_action',         name='order_action'),
    url(r'^orders/(\w+)/(\d+)/$',       'order_list',           name='order_list_client'),
    
    url(r'^pricelist/$',                'price_list',           name='price_list'),
    
    url(r'^clients/$',                  'client_list',          name='client_list'),
    url(r'^person/(\d+)/$',             'person_detail',        name='person_detail'),
    url(r'^person/search/$',            'person_search',        name='person_search'),
    url(r'^org/(\d+)/$',                'org_detail',           name='org_detail'),
    
    url(r'^reports/$',                  'report_list',          name='report_list'),
    url(r'^invoices/$',                 'invoice_list',         name='invoice_list'),
    url(r'^invoices/list/(\d+)/$',      'invoice_list',         name='invoice_list_order'),
    url(r'^invoices/(\d+)/$',           'invoice_detail',       name='invoice_detail'),
    url(r'^invoices/(\d+)/(add)/$',     'invoice_detail',       name='invoice_add'),
    url(r'^acts/$',                     'act_list',             name='act_list'),
    url(r'^acts/(\d+)/$',               'act_detail',           name='act_detail'),
    url(r'^analyze/$',                  'analyze',              name='analyze'),
    
    url(r'^print/(\w+)/(\d+)/$',        'document_print',       name='document_print'),
    
    url(r'^questions/$',                'question_list',        name='question_list'),
    
    url(r'^modal/(?P<obj>\w+)/(?P<key>\w+)/(?P<id>\d+)/$',
                                        'get_modal',            name='get_modal'),
)