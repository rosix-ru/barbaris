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
from django.db import models, connection, transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
import managers

import datetime, calendar

CLITYPE_PERSON = 1
CLITYPE_ORG = 2

class Client(models.Model):
    """ Клиент, как организация, так и частное лицо """
    
    CLITYPE_CHOICES = (
        (CLITYPE_PERSON,u'персона'),
        (CLITYPE_ORG,u'организация'),
    )
    clitype = models.IntegerField(
            choices=CLITYPE_CHOICES,
            #~ blank=True, null=True,
            verbose_name = u"тип")
    
    def __unicode__(self):
        client = self.client
        if client:
            return unicode(client)
        return self.get_clitype_display()
    
    class Meta:
        ordering = ['id']
        verbose_name = u"клиента"
        verbose_name_plural = u"клиенты"
    
    @models.permalink
    def get_absolute_url(self):
        client = self.client
        if client:
            if self.clitype == CLITYPE_PERSON:
                return ('person_detail', [str(client.id)])
            if self.clitype == CLITYPE_ORG:
                return ('org_detail', [str(client.id)])
        else:
            return ('client_create', [str(self.id)])
    
    @property
    def client(self):
        if self.clitype == CLITYPE_PERSON:
            try:
                return self.person
            except:
                return None
        
        if self.clitype == CLITYPE_ORG:
            try:
                return self.org
            except:
                return None
        
        return None
    
    @property
    def detail(self):
        return self.client
    
    def save(self, **kwargs):
        super(Client, self).save(**kwargs)
    
    def add_client(self):
        if not self.id:
            self.save()
        if not self.client:
            if self.clitype == CLITYPE_PERSON:
                client = Person(last_name=u'Новый клиент', client=self)
                client.save()
            elif self.clitype == CLITYPE_ORG:
                client = Org(title=u'Новый клиент', client=self)
                client.save()
        return self.client

class AbstractOrg(models.Model):
    """ Абстрактная модель организации """
    DOCUMENT_CHOICES = (
        (1,u'свидетельство'),
        (2,u'лицензия'),
    )
    title = models.CharField(
            max_length=100,
            verbose_name = u"название")
    fulltitle = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = u"полное название")
    inn = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"ИНН")
    kpp = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"КПП")
    ogrn = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"ОГРН")
    address = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = u"адрес")
    phones = models.CharField(
            max_length=100,
            blank=True,
            verbose_name = u"телефоны")
    
    # Банковские реквизиты
    bank_bik = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"БИК")
    bank_title = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = u"название банка")
    bank_set_account = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"Р/СЧ")
    bank_cor_account = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"КОР/СЧ")
    # Поля документа клиента
    document_type = models.IntegerField(
            choices=DOCUMENT_CHOICES,
            blank=True, null=True,
            verbose_name = u"тип")
    document_series = models.CharField(
            max_length=10,
            blank=True,
            verbose_name = u"серия")
    document_number = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"номер")
    document_date = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"дата выдачи")
    document_organ = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = u"орган выдачи")
    document_code = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"код органа")
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        abstract = True
    
    @property
    def get_string_requsites(self):
        return u', '.join([
            self.fulltitle, 
            u'ИНН '+self.inn,
            self.address,
        ])

class SelfOrg(AbstractOrg):
    """ Собственная организация-продавец услуг """
    is_active = models.BooleanField(
        default=True,
        verbose_name = u"активная")
    owner = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = u"владелец")
    class Meta:
        ordering = ['title']
        verbose_name = u"собственную фирму"
        verbose_name_plural = u"собственные фирмы"
    
    def save(self, **kwargs):
        super(SelfOrg, self).save(**kwargs)
        
        qs = SelfOrg.objects.filter(is_active=True)
        qs = qs.exclude(id=self.id)
        qs.update(is_active=False)

class Org(AbstractOrg):
    """ Организация-покупатель услуг """
    client = models.OneToOneField(Client,
        limit_choices_to={'clitype': CLITYPE_ORG },
        verbose_name=u"клиент",
        blank=True, null=True,
        )
    
    @property
    def org(self):
        return self
    
    class Meta:
        ordering = ['title']
        verbose_name = u"организацию"
        verbose_name_plural = u"организации"
    
    @models.permalink
    def get_absolute_url(self):
        return ('org_detail', [str(self.id)])
    
    def save(self, **kwargs):
        #~ if not self.client:
            #~ client = Client(clitype=CLITYPE_ORG)
            #~ client.save()
            #~ self.client = client
        super(Org, self).save(**kwargs)
    
class Person(models.Model):
    """ Физическое лицо, либо представитель фирмы """
    SEX_CHOICES = (
        (1,u'мужской'),
        (2,u'женский')
    )
    DOCUMENT_CHOICES = (
        (1,u'паспорт'),
        (2,u'военный билет'),
        (3,u'водительское удостоверение'),
    )
    last_name = models.CharField(
            max_length=50,
            verbose_name = u"фамилия")
    first_name = models.CharField(
            max_length=50,
            blank=True,
            verbose_name = u"имя")
    middle_name = models.CharField(
            max_length=50,
            blank=True,
            verbose_name = u"отчество")
    phones = models.CharField(
            max_length=50,
            blank=True,
            verbose_name = u"телефоны")
    sex = models.IntegerField(
            choices=SEX_CHOICES,
            blank=True, null=True,
            verbose_name = u"пол")
    org = models.ForeignKey(
            Org,
            null=True, blank=True,
            verbose_name = u"организация")
    # Поля места рождения
    birth_day = models.DateField(
            null=True, blank=True,
            verbose_name = u"дата")
    birth_country = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"страна")
    birth_region = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"регион")
    birth_area = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"район")
    birth_sity = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"город")
    birth_settlement = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"населённый пункт")
    
    # Поля места жительства
    residence_sitizenship = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"гражданство")
    residence_country = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"страна")
    residence_region = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"регион")
    residence_area = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"район")
    residence_sity = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"город")
    residence_settlement = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"населённый пункт")
    residence_street = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = u"улица")
    residence_house = models.CharField(
            max_length=8,
            blank=True,
            verbose_name = u"дом")
    residence_case = models.CharField(
            max_length=8,
            blank=True,
            verbose_name = u"корпус")
    residence_apartment = models.CharField(
            max_length=8,
            blank=True,
            verbose_name = u"квартира")
    # Поля документа клиента
    document_type = models.IntegerField(
            choices=DOCUMENT_CHOICES,
            blank=True, null=True,
            verbose_name = u"тип")
    document_series = models.CharField(
            max_length=10,
            blank=True,
            verbose_name = u"серия")
    document_number = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"номер")
    document_date = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"дата выдачи")
    document_organ = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = u"орган выдачи")
    document_code = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = u"код органа")
    
    client = models.OneToOneField(Client,
        limit_choices_to={'clitype': CLITYPE_PERSON },
        verbose_name=u"клиент",
        blank=True, null=True,
        )
    
    objects = models.Manager()
    privates = managers.PrivatePersonManager()
    
    def __unicode__(self):
        fio = u' '.join(
                [self.last_name, self.first_name, self.middle_name]
                ).replace("  ", ' ')
        return fio
        
    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']
        verbose_name = u"персону"
        verbose_name_plural = u"персоны"
    
    @property
    def residence_address(self):
        return ' '.join([
            self.residence_country,
            self.residence_region,
            self.residence_area,
            self.residence_sity,
            self.residence_settlement,
            ])
    
    @models.permalink
    def get_absolute_url(self):
        return ('person_detail', [str(self.id)])
    
    def save(self, **kwargs):
        #~ if not self.client:
            #~ client = Client(clitype=CLITYPE_PERSON)
            #~ client.save()
            #~ self.client = client
        super(Person, self).save(**kwargs)
    
class Category(models.Model):
    """ Категория услуги """
    title = models.CharField(
            choices = settings.CATEGORY_CHOICES,
            max_length=16,
            unique=True,
            verbose_name = u"название")
    
    def __unicode__(self):
        return self.get_title_display()
    
    class Meta:
        ordering = ['id']
        verbose_name = u"категорию"
        verbose_name_plural = u"категории"

class Service(models.Model):
    """ Услуга """
    category = models.ForeignKey(
            Category,
            verbose_name = u"категория")
    title = models.CharField(
            max_length=255,
            verbose_name = u"название")
    is_rooms = models.BooleanField(
            default=False,
            verbose_name = u"подразделяется на номера")
    is_reserved = models.BooleanField(
            default=False,
            verbose_name = u"разрешить бронирование")
    is_on_time = models.BooleanField(
            default=True,
            verbose_name = u"продажи по времени")
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = u"услугу"
        verbose_name_plural = u"услуги"
    
    @property
    def prices(self):
        prices = Price.actives.filter(service=self)
        return '; '.join([ 
            (p.get_divider_display() or u'Единица') +'='+ str(round(p.price, 2))
            for p in prices
            ])
    
    @property
    def active_prices(self):
        return Price.actives.filter(service=self)

class Room(models.Model):
    """ Гостиничные номера """
    service = models.ForeignKey(
            Service,
            limit_choices_to={'is_rooms': True},
            verbose_name = u"тип номера")
    num = models.IntegerField(
            unique=True,
            verbose_name = u"номер")
    
    def __unicode__(self):
        return str(self.num)
        
    class Meta:
        ordering = ['service', 'num']
        verbose_name = u"номер"
        verbose_name_plural = u"номера"
    
    @property
    def prices(self):
        return self.service.prices
    
    def orders(self, lookups=None):
        sps = Specification.objects.filter(room=self,
            order__state__in=settings.SELECT_WORK_ORDERS)
        for key, val in lookups.items():
            sps = sps.filter(models.Q(**{key: val}))
        list_id = [ x['order'] for x in sps.values('order')]
        orders = Order.objects.filter(id__in=list_id)
        return orders
        
    @property
    def current_order(self):
        now = datetime.datetime.now()
        orders = self.orders({'start__lte':now, 'end__gt':now})
        if orders:
            return orders[0]
        return None
    
    @property
    def next_orders(self):
        now = datetime.datetime.now()
        orders = self.orders({'start__gt':now, 'end__gt':now})
        #~ current = self.current_order
        #~ if current:
            #~ orders = orders.exclude(pk=current.pk)
        return orders
    
    @property
    def prew_orders(self):
        now = datetime.datetime.now()
        orders = self.orders({'end__lt':now})
        return orders
    
    @property
    def state(self):
        """ Получение статуса номера """
        now = datetime.datetime.now()
        day = now.date() + datetime.timedelta(days=1)
        current_order = self.current_order
        next_orders = self.next_orders
        released_order = self.orders({'start__lte':now, 'end__gte':now, 'end__lt':day})
        
        # Занят сейчас, но освобождается сегодня и:
        if released_order:
            # нет заказов на будущее.
            if not next_orders:
                return settings.STATE_ROOM_RELEASED_FREE
            # есть заказы на будущее.
            else:
                return settings.STATE_ROOM_RELEASED_NONFREE
        # Занят сейчас, но освобождается не сегодня и:
        elif current_order:
            # нет заказов на будущее.
            if not next_orders:
                return settings.STATE_ROOM_NONRELEASED_FREE
            # есть заказы на будущее.
            else:
                return settings.STATE_ROOM_NONRELEASED_NONFREE
        # Не занят сейчас и нет заказов на будущее
        elif not current_order:
            if not next_orders:
                return settings.STATE_ROOM_FREE
            else:
                return settings.STATE_ROOM_NONFREE
        else:
            assert current_order, "Ошибка в расчёте app.models.Room.state()"
    
class Price(models.Model):
    """ Цены на услуги """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True,editable=False)
    
    service = models.ForeignKey(
            Service,
            verbose_name = u"услуга")
    price = models.DecimalField(
            max_digits=10, decimal_places=2,
            default=0.0,
            verbose_name = u"цена")
    start_date = models.DateField(
            default=datetime.date.today() + datetime.timedelta(1),
            verbose_name = u"начало действия")
    divider = models.IntegerField(
            choices=settings.DIVIDER_PRICE_CHOICES,
            null=True, blank=True,
            verbose_name = u"делитель")
    
    objects = models.Manager()
    actives = managers.ActivePriceManager()
    
    def __unicode__(self):
        return self.service.title +': '+\
            (self.get_divider_display() or u'Единица') \
            +'='+ str(round(self.price, 2))
    
    class Meta:
        ordering = ['service__category__title','service','start_date',]
        verbose_name = u"цену"
        verbose_name_plural = u"цены"
        get_latest_by = 'start_date'
    
    def save(self, **kwargs):
        super(Price, self).save(**kwargs)
        
        qs = Price.actives.filter(service=self.service,
                                    divider=self.divider)
        try:
            latest = qs.latest()
            qs = qs.exclude(id=latest.id)
        except Price.DoesNotExist:
            pass
        qs.update(is_active=False)
    
    def category(self):
        return unicode(self.service.category)

class Reservation(models.Model):
    """ Вид бронирования и его процентная надбавка"""
    title = models.CharField(
            max_length=255,
            verbose_name = u"название")
    expired_days = models.IntegerField(
            default=0,
            verbose_name = u"истечение в днях")
    percent = models.DecimalField(
            max_digits=3, decimal_places=2,
            verbose_name = u"процент надбавки",
            help_text='"10%" это "0.10"')
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = u"вид бронирования"
        verbose_name_plural = u"виды бронирования"

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(
            User,
            verbose_name=u"пользователь")
    state = models.IntegerField(
            choices=settings.STATE_ORDER_CHOICES,
            default=1,
            verbose_name=u"состояние")
    clients = models.ManyToManyField(
            Client,
            null=True, blank=True,
            verbose_name=u"персоны")
    is_divdoc = models.BooleanField(
            default=False,
            verbose_name = u"разделять документы на персон")
    comment = models.TextField(
            blank=True,
            verbose_name=u"комментарий")
    
    start = models.DateTimeField(
            null=True, blank=True,
            verbose_name = u"начало")
    end = models.DateTimeField(
            null=True, blank=True,
            verbose_name = u"окончание")
    
    objects  = models.Manager()
    creates  = managers.CreateOrderManager()
    accepts  = managers.AcceptOrderManager()
    closes   = managers.CloseOrderManager()
    cancels  = managers.CancelOrderManager()
    workeds  = managers.WorkOrderManager()
    
    def __unicode__(self):
        return u'Заказ №%s от %sг.' % (
            self.id,
            self.created.strftime("%d.%m.%Y")
        )
    
    class Meta:
        ordering = ['-id']
        verbose_name = u"заказ"
        verbose_name_plural = u"заказы"
        get_latest_by = 'updated'
    
    @property
    def summa(self):
        return sum([ x.summa for x in self.specification_set.all() ])
    
    @property
    def summa_for_client(self):
        if not self.is_divdoc:
            return self.summa
        return self.summa / self.clients.count()
    @property
    def payment(self):
        payments = Payment.objects.filter(invoice__order=self)
        return sum([ x.summa for x in payments.filter(is_paid=True) ])
    @property
    def payment_cash(self):
        payments = Payment.objects.filter(invoice__order=self, payment=settings.PAYMENT_INVOICE_CASH)
        return sum([ x.summa for x in payments.filter(is_paid=True) ])
    @property
    def payment_cashless(self):
        payments = Payment.objects.filter(invoice__order=self, payment=settings.PAYMENT_INVOICE_CASHLESS)
        return sum([ x.summa for x in payments.filter(is_paid=True) ])
    @property
    def payment_card(self):
        payments = Payment.objects.filter(invoice__order=self, payment=settings.PAYMENT_INVOICE_CARD)
        return sum([ x.summa for x in payments.filter(is_paid=True) ])
    @property
    def debet(self):
        return float(self.summa) - float(self.payment)
    
    @property
    def invoices(self):
        return self.invoice_set.all()
    
    @property
    def acts(self):
        return self.act_set.all()

    @property
    def state_create(self):
        return self.state == settings.STATE_ORDER_CREATE
    @property
    def state_accept(self):
        return self.state == settings.STATE_ORDER_ACCEPT
    @property
    def state_close(self):
        return self.state == settings.STATE_ORDER_CLOSE
    @property
    def state_cancel(self):
        return self.state == settings.STATE_ORDER_CANCEL
    
    def save(self, **kwargs):
        # Устанавливаем начало и конец действия заказа по 
        # минимальному значению начала спецификаций
        # и по максимальному их конца
        sps = self.specification_set.all()
        try:
            sp = sps.filter(start__isnull=False).order_by('start')[0]
            start = sp.start
        except:
            start = None
        try:
            sp = sps.filter(end__isnull=False).order_by('-end')[0]
            end = sp.end
        except:
            end = None
        self.start = start or self.updated
        self.end = end or self.updated
        
        # Закрытие заказа
        if self.state_accept and self.debet <= 0 and self.specification_set.count():
            self.state = settings.STATE_ORDER_CLOSE
        
        super(Order, self).save(**kwargs)
    
    @property
    def numbers(self):
        sps = self.specification_set.filter(room__isnull=False)
        L = [str(x.room.num) for x in sps]
        return u', '.join(set(L))
    
class Specification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    order = models.ForeignKey(
            Order,
            verbose_name=u"заказ")
    price = models.ForeignKey(
            Price,
            verbose_name=u"услуга")
    room = models.ForeignKey(
            Room,
            null=True, blank=True,
            verbose_name=u"номер")
    count = models.IntegerField(
            null=True, blank=True,
            verbose_name=u"количество")
    start = models.DateTimeField(
            null=True, blank=True,
            verbose_name = u"начало")
    end = models.DateTimeField(
            null=True, blank=True,
            verbose_name = u"окончание")
    reservation = models.ForeignKey(
            Reservation,
            null=True, blank=True,
            verbose_name=u"бронирование")
    
    objects  = models.Manager()
    workeds  = managers.WorkSpecificationManager()
    
    def __unicode__(self):
        return unicode(self.price)
    
    class Meta:
        ordering = ['order', '-updated',]
        verbose_name = u"спецификацию"
        verbose_name_plural = u"спецификации"
    
    def markup(self):
        if self.reservation and self.price.service.is_reserved:
            markup = self.price.price*self.reservation.percent
        else:
            markup = 0
        return markup
    
    def markup_for_client(self):
        if not self.order.is_divdoc:
            return self.markup()
        return round((self.markup() /  self.order.clients.count()), 2)
    
    @property
    def price_for_client(self):
        if not self.order.is_divdoc:
            return round(self.price.price, 2)
        return round((self.price.price /  self.order.clients.count()), 2)
    
    @property
    def summa(self):
        return round((self.price.price*self.count)+self.markup(), 2)
    @property
    def summa_for_client(self):
        if not self.order.is_divdoc:
            return self.summa
        return round((self.summa /  self.order.clients.count()), 2)
    
    @property
    def summa_clean(self):
        return round((self.price.price*self.count), 2)
    @property
    def summa_clean_for_client(self):
        if not self.order.is_divdoc:
            return self.summa_clean
        return round((self.summa_clean /  self.order.clients.count()), 2)
    
    @property
    def summa_markup(self):
        return round(self.markup(), 2)
    
    @property
    def summa_markup_for_client(self):
        if not self.order.is_divdoc:
            return self.summa_markup
        return round((self.summa_markup / self.order.clients.count()), 2)
    
    def save(self, **kwargs):
        """ Если есть делитель и услуга предоставляется по времени:
            Получаем старый объект, сравниваем изменившееся
            приоритетное поле count.
            
            Если количество отсутствует либо не изменилось,
            то по интервалу времени и делителю устанавливаем количество.
            Если же интервал тоже отсутствует, то количество 
            выставляем равным единице, и снова пытаемся установить
            интервал согласно делителя, количества и текущего времени.
            
            Наоборот, если есть количество,
            то рассчитываем интервал согласно делителя.
        """
        
        def add_months(dt, count):
            _year = dt.year + (dt.month + count) / 12
            _month = (dt.month + count) % 12 or 12
            for i in range(0,4):
                try:
                    return dt.replace(_year, _month, dt.day-i)
                except:
                    continue
        
        def get_end(start, count):
            d = self.price.divider
            if d == settings.DIVIDER_DAY:
                return start + datetime.timedelta(days=count)
            elif d == settings.DIVIDER_HOUR:
                return start + datetime.timedelta(hours=count)
            elif d == settings.DIVIDER_MONTH:
                return add_months(start, count)
            else:
                return start
        
        def roundTime(dt=None, roundTo=60):
            """Round a datetime object to any time laps in seconds
            dt : datetime.datetime object, default now.
            roundTo : Closest number of seconds to round to, default 1 minute.
            Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            """
            if dt == None : dt = datetime.datetime.now()
            seconds = (dt - dt.min).seconds
            # // is a floor division, not a comment on following line:
            rounding = (seconds+roundTo/2) // roundTo * roundTo
            return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
 
        def set_interval():
            #~ print 'def set_interval()' # DEBUG
            if not self.count or not self.price.divider:
                return False
            if self.start:
                start = self.start.replace(second=0)
            else:
                start = None
            self.start = start or roundTime()
            self.end = get_end(self.start, self.count)
            
            # Установка расчётного времени на вторые и более сутки
            # для номеров
            if self.room and self.count > 1 and settings.ESTIMATED_TIME \
            and self.price.divider == settings.DIVIDER_DAY:
                self.end = self.end.replace(
                    hour=settings.ESTIMATED_TIME_HOUR,
                    minute=settings.ESTIMATED_TIME_MINUTE)
            
            return True
        
        def get_divider_sec():
            d = self.price.divider
            if d == settings.DIVIDER_DAY:
                return 24*60*60 # часы*минуты*секунды
            elif d == settings.DIVIDER_HOUR:
                return 60*60 # минуты*секунды
            elif d == settings.DIVIDER_MONTH:
                days = calendar.monthrange(self.start.year, self.start.month)
                return days*24*60*60 # дни*часы*минуты*секунды
            else:
                return 0
        
        def set_count():
            #~ print 'def set_count()' # DEBUG
            ds = get_divider_sec()
            if not self.end or not ds:
                #~ print "if not self.end or not ds" # DEBUG
                return False
            self.start = self.start or roundTime()
            delta = self.end - self.start
            count = int(round((delta.seconds + delta.days*60*60*24) / ds))
            if not count:
                return False
            self.count = count
            return True
        
        if self.price.divider and self.price.service.is_on_time:
            if self.id:
                old = Specification.objects.get(id=self.id)
                change_count = bool(self.count != old.count)
            else:
                change_count = bool(self.count)
            if not change_count:
                #~ print "if not change_count" # DEBUG
                if not set_count():
                    #~ print "if not set_count()" # DEBUG
                    self.count = 1
                    if not set_interval():
                        print u'ошибка изменения спецификации'
                        return False
            else:
                #~ print "else" # DEBUG
                if not set_interval():
                    if not set_count():
                        print u'ошибка изменения спецификации'
                        return False
        
        super(Specification, self).save(**kwargs)
        
        # Заказ помечается как принятый, при любых изменениях 
        # после первичного принятия
        if not self.order.state_create:
            self.order.state = settings.STATE_ORDER_ACCEPT
            self.order.save()
    
    def delete(self, **kwargs):
        # Заказ помечается как принятый, при любых изменениях 
        # после первичного принятия
        self.order.state = settings.STATE_ORDER_ACCEPT
        self.order.save()
        super(Specification, self).delete(**kwargs)
    
class DocTemplate(models.Model):
    """ Шаблоны актов и счетов """
    title = models.CharField(
            max_length=100,
            verbose_name = u"название")
    document = models.CharField(
            max_length=16,
            choices=settings.DOCUMENT_CHOICES,
            verbose_name = u"вид документа")
    is_default = models.BooleanField(
            default=True,
            verbose_name = u"по-умолчанию")
    fname = models.CharField(
            max_length=100,
            blank=True,
            verbose_name = u"имя файла шаблона")
    text = models.TextField(
            blank=True,
            verbose_name = u"шаблон документа")
    
    def __unicode__(self):
        return unicode(self.title)
    
    class Meta:
        ordering = ['title', 'document' ]
        verbose_name = u"шаблон документа"
        verbose_name_plural = u"шаблоны документов"
    
    def save(self, **kwargs):
        if self.is_default:
            docs = DocTemplate.objects.filter(document=self.document, is_default=True)
            docs.update(is_default=False)
        super(DocTemplate, self).save(**kwargs)

class Invoice(models.Model):
    """ Счёт на оплату """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(
            User,
            verbose_name=u"пользователь")
    state = models.IntegerField(
            choices=settings.STATE_INVOICE_CHOICES,
            default=1,
            verbose_name = u"состояние")
    order = models.ForeignKey(
            Order,
            verbose_name = u"заказ")
    client = models.ForeignKey(
            Client,
            null=True, blank=True,
            verbose_name=u"клиент")
    date = models.DateField(
            null=True, blank=True,
            verbose_name = u"дата документа")
    summa = models.DecimalField(
            max_digits=10, decimal_places=2,
            default=0.0,
            verbose_name = u"сумма",
            help_text=u'Установите 0 для автоматического расчёта.')
    comment = models.TextField(
            blank=True,
            verbose_name = u"комментарий")
    
    objects = models.Manager()
    payments = managers.PaymentInvoiceManager()
    avances = managers.AvanceInvoiceManager()
    cashes = managers.CashInvoiceManager()
    
    def __unicode__(self):
        return u'Счёт №%s от %s %s' % (
            unicode(self.id),
            self.date.strftime("%d.%m.%Y"),
            unicode(self.client),
            )
    
    class Meta:
        ordering = ['user', '-created',]
        verbose_name = u"счёт"
        verbose_name_plural = u"счета"
    
    def save(self, **kwargs):
        if not self.summa:
            if self.order.is_divdoc:
                self.summa = str(self.order.summa_for_client)
            else:
                self.summa = str(self.order.summa)
        
        super(Invoice, self).save(**kwargs)
        
        self.order.save()
    
    @property
    def summa_float(self):
        return float(self.summa)
    
    @property
    def document(self):
        return u'Счёт'
    
    @property
    def document_type(self):
        return u'invoice'
    
    @property
    def state_create(self):
        return self.state == settings.STATE_INVOICE_CREATE
    @property
    def state_payment(self):
        return self.state == settings.STATE_INVOICE_PAYMENT
    @property
    def state_avance(self):
        return self.state == settings.STATE_INVOICE_AVANCE
    
    #~ @property
    #~ def summa(self):
        #~ return self.order.summa
    @property
    def payment(self):
        return sum([ x.summa for x in self.payment_set.filter(is_paid=True) ])
    @property
    def payment_cash(self):
        return sum([ x.summa for x in self.payment_set.filter(is_paid=True, payment=settings.PAYMENT_INVOICE_CASH) ])
    @property
    def payment_cashless(self):
        return sum([ x.summa for x in self.payment_set.filter(is_paid=True, payment=settings.PAYMENT_INVOICE_CASHLESS) ])
    @property
    def payment_card(self):
        return sum([ x.summa for x in self.payment_set.filter(is_paid=True, payment=settings.PAYMENT_INVOICE_CARD) ])
    @property
    def debet(self):
        return float(self.summa) - float(self.payment)
    
class Payment(models.Model):
    """ Приходный ордер """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(
            User,
            verbose_name=u"пользователь")
    payment = models.IntegerField(
            choices=settings.PAYMENT_INVOICE_CHOICES,
            default=1,
            verbose_name = u"вид расчёта")
    invoice = models.ForeignKey(
            Invoice,
            verbose_name = u"счёт")
    summa = models.DecimalField(
            max_digits=10, decimal_places=2,
            default=0.0,
            verbose_name = u"сумма")
    comment = models.TextField(
            blank=True,
            verbose_name = u"комментарий")
    is_paid = models.BooleanField(
        default=False,
        verbose_name = u"оплата подтверждена",
        )
    
    def __unicode__(self):
        return u'Оплата №%s по счёту №%s от %s' % (
            unicode(self.id),
            unicode(self.invoice.id),
            self.invoice.date.strftime("%d.%m.%Y"),
            )
    
    class Meta:
        ordering = ['user', '-created',]
        verbose_name = u"приходный ордер"
        verbose_name_plural = u"приходные ордеры"
    
    def save(self, **kwargs):
        if not self.summa:
            self.summa = str(self.invoice.debet)
        
        super(Payment, self).save(**kwargs)
        
        if self.is_paid:
            if float(self.summa) >= float(self.invoice.debet):
                self.invoice.state = settings.STATE_INVOICE_PAYMENT
            else:
                self.invoice.state = settings.STATE_INVOICE_AVANCE
            self.invoice.save()
                
    def delete(self, **kwargs):
        order = self.invoice.order
        super(Payment, self).delete(**kwargs)
        order.save()
    
    @property
    def document(self):
        return u'Приходный ордер'
    
    @property
    def document_type(self):
        return u'payment'

class Act(models.Model):
    """ Акт выполненных работ """
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
            User,
            verbose_name=u"пользователь")
    order = models.ForeignKey(
            Order,
            verbose_name = u"заказ")
    invoice = models.ForeignKey(
            Invoice,
            null=True, blank=True,
            verbose_name=u"счёт")
    client = models.ForeignKey(
            Client,
            null=True, blank=True,
            verbose_name=u"клиент")
    date = models.DateField(
            null=True, blank=True,
            verbose_name = u"дата документа")
    comment = models.TextField(
            blank=True,
            verbose_name = u"комментарий")
    
    def __unicode__(self):
        return u'Акт №%s от %s' % (
            unicode(self.id),
            self.date.strftime("%d.%m.%Y"),
            )
    
    class Meta:
        ordering = ['user', '-created']
        verbose_name = u"акт"
        verbose_name_plural = u"акты"
    
    @property
    def document(self):
        return u'Акт выполненных работ'
    
    @property
    def document_type(self):
        return u'act'

class Question(models.Model):
    """ Вопросы """
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
            User,
            verbose_name=u"пользователь")
    theme = models.CharField(
            max_length=100,
            verbose_name = u"тема вопроса")
    text = models.TextField(
            verbose_name = u"текст вопроса")
    
    def __unicode__(self):
        return self.text
    
    class Meta:
        ordering = ['-created']
        verbose_name = u"вопрос"
        verbose_name_plural = u"вопросы"

class Answer(models.Model):
    """ Ответы """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    question = models.ForeignKey(
            Question,
            verbose_name=u"вопрос")
    user = models.ForeignKey(
            User,
            verbose_name=u"пользователь")
    text = models.TextField(
            verbose_name = u"текст ответа")
    
    def __unicode__(self):
        return self.text
    
    class Meta:
        ordering = ['-updated']
        verbose_name = u"ответ"
        verbose_name_plural = u"ответы"
