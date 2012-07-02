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

class CreatedOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CreatedOrderManager, self).get_query_set().filter(
            state=settings.CREATED_ORDER
        )

class AvansedOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CreatedOrderManager, self).get_query_set().filter(
            state=settings.AVANCED_ORDER
        )

class PayedOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CreatedOrderManager, self).get_query_set().filter(
            state=settings.PAYED_ORDER
        )

class CancelledOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CreatedOrderManager, self).get_query_set().filter(
            state=settings.CANCELLED_ORDER
        )

class WorkedOrderManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(CreatedOrderManager, self).get_query_set().filter(
            state__in=settings.SELECT_WORKED_ORDERS
        )
