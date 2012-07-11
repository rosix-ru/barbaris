# -*- coding: utf-8 -*-
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

class CreateOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CreateOrderManager, self).get_query_set().filter(
            state=settings.CREATE_ORDER
        )

class ReservOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(ReservOrderManager, self).get_query_set().filter(
            state=settings.RESERV_ORDER
        )

class AcceptOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(AcceptOrderManager, self).get_query_set().filter(
            state=settings.ACCEPT_ORDER
        )

class AvanseOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(AvanceOrderManager, self).get_query_set().filter(
            state=settings.AVANCE_ORDER
        )

class PaymentOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(PaymentOrderManager, self).get_query_set().filter(
            state=settings.PAYMENT_ORDER
        )

class CancelOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CancelOrderManager, self).get_query_set().filter(
            state=settings.CANCEL_ORDER
        )

class WorkOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(WorkOrderManager, self).get_query_set().filter(
            state__in=settings.SELECT_WORKED_ORDERS
        )

class SellerOrganizationManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(SellerOrganizationManager, self).get_query_set().filter(
            is_seller=True
        )

class BuyerOrganizationManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(BuyerOrganizationManager, self).get_query_set().filter(
            is_seller=False
        )

class PrivateClientManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(PrivateClientManager, self).get_query_set().filter(
            organization=None
        )
