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

urlpatterns = patterns('barbaris.online.views',
    url(r'^$', 'monitor', name='monitor'),
    url(r'^orders/$', 'orders', name='orders'),
    url(r'^orders/(\w+)/(\d+)/$', 'orders', name='client_orders'),
    url(r'^order/new/(\w+)/(\d+)/$', 'new_order', name='new_order'),
    url(r'^pricelist/$', 'pricelist', name='pricelist'),
    url(r'^invoices/$', 'invoices', name='invoices'),
    url(r'^acts/$', 'acts', name='acts'),
    url(r'^clients/$', 'clients', name='clients'),
    url(r'^client/(\d+)/$', 'client_detail', name='client_detail'),
    url(r'^org/(\d+)/$', 'org_detail', name='org_detail'),
    url(r'^analyze/$', 'analyze', name='analyze'),
    url(r'^reports/$', 'reports', name='reports'),
    url(r'^questions/$', 'questions', name='questions'),
)
