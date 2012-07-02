# -*- coding: utf-8 -*-
from django.db import models, connection, transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from barabris.online.managers import ActivePriceManager,\
    CreatedOrderManager, AvansedOrderManager, \
    PayedOrderManager, CancelledOrderManager, WorkedOrderManager

import datetime

class Organization(models.Model):
    """ Фирма - клиент """
    title = models.CharField(
            max_length=255,
            verbose_name = _('title'))
    inn = models.CharField(
            max_length=16,
            unique=True,
            verbose_name=_('INN'))
    address = models.CharField(
            max_length=255,
            blank=True,
            verbose_name=_('address'))
    phones = models.CharField(
            max_length=50,
            blank=True,
            verbose_name=_('phones'))
    details = models.TextField(
            blank=True,
            verbose_name=_('details'))
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

class Client(models.Model):
    """ Клиент - физическое лицо, либо представитель фирмы"""
    organization = models.ForeignKey(
            Organization,
            null=True, blank=True,
            verbose_name = _('organization'))
    last_name = models.CharField(
            max_length=50,
            blank=True,
            verbose_name=_('last name'))
    first_name = models.CharField(
            max_length=50,
            blank=True,
            verbose_name=_('first name'))
    middle_name = models.CharField(
            max_length=50,
            blank=True,
            verbose_name=_('last name'))
    birth = models.DateField(
            blank=True,
            verbose_name=_('date of birth'))
    phones = models.CharField(
            max_length=50,
            blank=True,
            verbose_name=_('phones'))
    details = models.TextField(
            blank=True,
            verbose_name=_('details'))
    
    def __unicode__(self):
        fio = u' '.join(
                [self.last_name, self.first_name, self.middle_name]
                ).replace("  ", ' ')
        if not fio and self.organization:
            return self.organization
        else:
            return fio
        
    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']
        verbose_name = _('client')
        verbose_name_plural = _('clients')

class Category(models.Model):
    """ Категория услуги """
    title = models.CharField(
            max_length=255,
            verbose_name = _('title'))
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

class Service(models.Model):
    """ Услуга """
    category = models.ForeignKey(
            Category,
            verbose_name = _('category'))
    title = models.CharField(
            max_length=255,
            verbose_name = _('title'))
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _('service')
        verbose_name_plural = _('services')

class Price(models.Model):
    """ Цены на услуги """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True,editable=False)
    
    service = models.ForeignKey(
            Service,
            verbose_name = _('service'))
    price = models.DecimalField(
            max_digits=10, decimal_places=2,
            default=0.0,
            verbose_name = _('price'))
    start_date = models.DateField(
            default=datetime.date.today() +1,
            verbose_name = _('start date'))
    
    objects = models.Manager()
    actives = ActivePriceManager()
    
    def __unicode__(self):
        return unicode(self.service)
    
    class Meta:
        ordering = ['service','start_date',]
        verbose_name = _('price')
        verbose_name_plural = _('prices')
        get_latest_by = 'start_date'
    
    def save(self, **kwargs):
        super(Price, self).save(**kwargs)
        
        qs = Price.actives.filter(service=self.service)
        try:
            latest = qs.latest()
            qs = qs.exclude(id=latest.id)
        except Price.DoesNotExist:
            pass
        qs.update(is_active=False)

class Brone(models.Model):
    """ Вид бронирования """
    title = models.CharField(
            max_length=255,
            verbose_name=_('title'))
    expired_days = models.IntegerField(
            verbose_name=_('expired days'))
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _('brone')
        verbose_name_plural = _('brones')
    
class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    state = models.IntegerField(
            choices=settings.ORDER_STATE_CHOICES,
            default=1,
            verbose_name=_('state'))
    client = models.ForeignKey(
            Client,
            verbose_name=_('client'))
    start_date = models.DateField(
            default=datetime.date.today(),
            verbose_name = _('start date'))
    start_time = models.TimeField(
            default=datetime.datetime.now(),
            verbose_name = _('start time'))
    brone = models.ForeignKey(
            Brone,
            verbose_name=_('brone'))
    comment = models.CharField(
            max_length=255,
            blank=True,
            verbose_name=_('comment'))
            
    objects = models.Manager()
    creates = CreatedOrderManager()
    avances = AvansedOrderManager()
    payeds  = PayedOrderManager()
    cancels = CancelledOrderManager()
    workeds = WorkedOrderManager()
    
    def __unicode__(self):
        return unicode(self.client)
    
    class Meta:
        ordering = ['-updated', 'client']
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        get_latest_by = 'updated'
    
    @property
    def summa(self):
        return sum([ x.summa for x in self.specification_set.all() ])
    
class Specification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    order = models.ForeignKey(
            Order,
            verbose_name=_('order'))
    price = models.ForeignKey(
            Price,
            verbose_name=_('price'))
    quantity = models.IntegerField(
            default=0,
            verbose_name=_('quantity'))
    
    def __unicode__(self):
        return unicode(self.price)
    
    class Meta:
        ordering = ['order', '-updated',]
        verbose_name = _('specification')
        verbose_name_plural = _('specifications')
    
    @property
    def summa(self):
        return self.price.price*self.quantity
    
class Invoice(models.Model):
    """ Счёт """
    created = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        verbose_name=_('created'))
    client = models.ForeignKey(
            Client,
            verbose_name=_('client'))
    order = models.ForeignKey(
            Order,
            null=True, blank=True,
            verbose_name=_('order'))
    summa = models.DecimalField(
            max_digits=10, decimal_places=2,
            default=0.0,
            verbose_name = _('summa'))
    comment = models.CharField(
            max_length=255,
            blank=True,
            verbose_name=_('comment'))
    
    def __unicode__(self):
        return unicode(self.client)
    
    class Meta:
        ordering = ['client', 'order']
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
    
    def save(self, **kwargs):
        if not self.summa and self.order:
            self.summa = self.order.summa
        super(Invoice, self).save(**kwargs)
