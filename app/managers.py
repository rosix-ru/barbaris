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
from django.db import models
from django.conf import settings

import datetime

class ActivePriceManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(ActivePriceManager, self).get_query_set().filter(
            is_active=True,
            start_date__lte=datetime.date.today()
        )

class ActiveOrgDetailManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(ActiveOrgDetailManager, self).get_query_set().filter(
            is_active=True
        )

class ActivePersonDetailManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(ActivePersonDetailManager, self).get_query_set().filter(
            is_active=True
        )

class CreateOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CreateOrderManager, self).get_query_set().filter(
            state=settings.STATE_ORDER_CREATE
        )

class AcceptOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(AcceptOrderManager, self).get_query_set().filter(
            state=settings.STATE_ORDER_ACCEPT
        )

class CloseOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CloseOrderManager, self).get_query_set().filter(
            state=settings.STATE_ORDER_CLOSE
        )

class CancelOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CancelOrderManager, self).get_query_set().filter(
            state=settings.STATE_ORDER_CANCEL
        )

class WorkOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(WorkOrderManager, self).get_query_set().filter(
            state__in=settings.SELECT_WORK_ORDERS
        )

class WorkSpecificationManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(WorkSpecificationManager, self).get_query_set().filter(
            order__state__in=settings.SELECT_WORK_ORDERS
        )

class CreateInvoiceManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CreateInvoiceManager, self).get_query_set().filter(
            state=settings.STATE_INVOICE_CREATE
        )

class PaymentInvoiceManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(PaymentInvoiceManager, self).get_query_set().filter(
            state=settings.STATE_INVOICE_PAYMENT
        )

class AvanceInvoiceManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(AvanceInvoiceManager, self).get_query_set().filter(
            state=settings.STATE_INVOICE_AVANCE
        )

class CashInvoiceManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CashInvoiceManager, self).get_query_set().filter(
            state__in=settings.SELECT_CASH_INVOICES
        )

class SellerOrgManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(SellerOrgManager, self).get_query_set().filter(
            is_seller=True
        )

class BuyerOrgManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(BuyerOrgManager, self).get_query_set().filter(
            is_seller=False
        )

class PrivatePersonManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(PrivatePersonManager, self).get_query_set().filter(
            org=None
        )
