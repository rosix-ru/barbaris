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

from django.db import models, connection, transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
import managers

import datetime, calendar

class Org(models.Model):
    """ Представляет собственную организацию-продавца услуг(seller),
        либо покупателя.
    """
    is_seller = models.BooleanField(
            default=False,
            verbose_name = u"продавец")
    title = models.CharField(
            max_length=100,
            verbose_name = u"название")
    
    objects = models.Manager()
    sellers = managers.SellerOrgManager()
    buyers  = managers.BuyerOrgManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = u"организацию"
        verbose_name_plural = u"организации"
    
    @property
    def detail(self):
        try:
            return self.orgdetail_set.get(is_active=True)
        except:
            return OrgDetail.objects.create(org=self)
    
    @models.permalink
    def get_absolute_url(self):
        return ('org_detail', [str(self.id)])
    
class OrgDetail(models.Model):
    """ Расширенная информация об организации """
    is_active = models.BooleanField(
            default=True,
            verbose_name = u"активная")
    org = models.ForeignKey(
            Org,
            verbose_name = u"организация")
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
    # Поля документа организации
    document_type = models.CharField(
            max_length=50,
            blank=True,
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
    
    objects = models.Manager()
    actives = managers.ActiveOrgDetailManager()
    
    def __unicode__(self):
        return unicode(self.org)
        
    class Meta:
        ordering = ['org',]
        verbose_name = u"карточку организации"
        verbose_name_plural = u"карточки организаций"
    
    def save(self, **kwargs):
        super(OrgDetail, self).save(**kwargs)
        
        qs = OrgDetail.actives.filter(org=self.org)
        qs = qs.exclude(id=self.id)
        qs.update(is_active=False)
    
    @property
    def get_string_requsites(self):
        return u', '.join([
            self.fulltitle, 
            u'ИНН '+self.inn,
            self.address,
        ])
    
class Person(models.Model):
    """ Клиент - физическое лицо, либо представитель фирмы, 
        который может быть представлен существительным во 
        множественном числе, например: "нефтяники", в 
        обязательном поле last_name.
    """
    SEX_CHOICES = (
        (u'муж',u'мужской'),
        (u'жен',u'женский')
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
    sex = models.CharField(
            max_length=3,
            choices=SEX_CHOICES,
            blank=True,
            verbose_name = u"пол")
    org = models.ForeignKey(
            Org,
            null=True, blank=True,
            verbose_name = u"организация")
    
    objects = models.Manager()
    privates = managers.PrivatePersonManager()
    
    def __unicode__(self):
        fio = u' '.join(
                [self.last_name, self.first_name, self.middle_name]
                ).replace("  ", ' ')
        return fio
        
    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']
        verbose_name = u"клиента"
        verbose_name_plural = u"клиенты"
    
    @property
    def detail(self):
        try:
            return self.persondetail_set.get(is_active=True)
        except:
            return PersonDetail.objects.create(person=self)
    
    @models.permalink
    def get_absolute_url(self):
        return ('person_detail', [str(self.id)])

class PersonDetail(models.Model):
    """ Расширенная информация о клиенте """
    
    DOCUMENT_CHOICES = (
        ('паспорт','паспорт'),
        ('водительское','водительское удостоверение')
    )
    is_active = models.BooleanField(
            default=True,
            verbose_name = u"активная")
    person = models.ForeignKey(
            Person,
            verbose_name = u"клиент")
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
    # Поля документа клиента
    document_type = models.CharField(
            max_length=16,
            choices=DOCUMENT_CHOICES,
            blank=True,
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
    
    objects = models.Manager()
    actives = managers.ActivePersonDetailManager()
    
    def __unicode__(self):
        return unicode(self.person)
        
    class Meta:
        ordering = ['person',]
        verbose_name = u"карточку клиента"
        verbose_name_plural = u"карточки клиентов"
    
    def save(self, **kwargs):
        super(PersonDetail, self).save(**kwargs)
        
        qs = PersonDetail.actives.filter(person=self.person)
        qs = qs.exclude(id=self.id)
        qs.update(is_active=False)
    
    @property
    def residence_address(self):
        return ' '.join([
            self.residence_country,
            self.residence_region,
            self.residence_area,
            self.residence_sity,
            self.residence_settlement,
            ])
    
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
        return '%s: %s' % (unicode(self.category), self.title)
        
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
    def price(self):
        return self.service.price

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

class Attribute(models.Model):
    value = models.IntegerField(
            choices=settings.ATTRIBUTE_CHOICES,
            unique=True,
            verbose_name = u"значение")
    
    def __unicode__(self):
        return self.value
        
    class Meta:
        ordering = ['value']
        verbose_name = u"атрибут"
        verbose_name_plural = u"атрибуты"

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(
            User,
            verbose_name="пользователь")
    state = models.IntegerField(
            choices=settings.STATE_ORDER_CHOICES,
            default=1,
            verbose_name="состояние")
    person = models.ForeignKey(
            Person,
            null=True, blank=True,
            verbose_name="клиент")
    other_persons = models.ManyToManyField(
            Person,
            null=True, blank=True,
            related_name = 'order_other_set',
            verbose_name = u"другие клиенты")
    attributes = models.ManyToManyField(
            Attribute,
            null=True, blank=True,
            verbose_name = u"атрибуты")
    comment = models.TextField(
            blank=True,
            verbose_name="комментарий")
    
    
    objects  = models.Manager()
    creates  = managers.CreateOrderManager()
    accepts  = managers.AcceptOrderManager()
    avances  = managers.AvanceOrderManager()
    closes   = managers.CloseOrderManager()
    cancels  = managers.CancelOrderManager()
    workeds  = managers.WorkOrderManager()
    
    def __unicode__(self):
        return unicode(self.person)
    
    class Meta:
        ordering = ['-updated', 'person']
        verbose_name = u"заказ"
        verbose_name_plural = u"заказы"
        get_latest_by = 'updated'
    
    @property
    def summa(self):
        return sum([ x.summa for x in self.specification_set.all() ])
    
    @property
    def state_create(self):
        return self.state == settings.STATE_ORDER_CREATE
    @property
    def state_accept(self):
        return self.state == settings.STATE_ORDER_ACCEPT
    @property
    def state_avance(self):
        return self.state == settings.STATE_ORDER_AVANCE
    @property
    def state_close(self):
        return self.state == settings.STATE_ORDER_CLOSE
    @property
    def state_cancel(self):
        return self.state == settings.STATE_ORDER_CANCEL
    
class Specification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    order = models.ForeignKey(
            Order,
            verbose_name="заказ")
    price = models.ForeignKey(
            Price,
            verbose_name="услуга")
    room = models.ForeignKey(
            Room,
            null=True, blank=True,
            verbose_name="номер")
    count = models.IntegerField(
            null=True, blank=True,
            verbose_name="количество")
    start = models.DateTimeField(
            null=True, blank=True,
            verbose_name = u"начало")
    end = models.DateTimeField(
            null=True, blank=True,
            verbose_name = u"окончание")
    reservation = models.ForeignKey(
            Reservation,
            null=True, blank=True,
            verbose_name="бронирование")
    
    def __unicode__(self):
        return unicode(self.price)
    
    class Meta:
        ordering = ['order', '-updated',]
        verbose_name = u"спецификацию"
        verbose_name_plural = u"спецификации"
    
    @property
    def summa(self):
        if self.reservation and self.price.service.is_reserved:
            markup = self.price.price*self.reservation.percent
        else:
            markup = 0
        return round((self.price.price*self.count)+markup, 2)
    
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
        
        def set_interval():
            print 'def set_interval()' # DEBUG
            ds = get_divider_sec()
            if not self.count or not ds:
                return False
            self.start = self.start or datetime.datetime.now()
            delta = datetime.timedelta(seconds=ds*self.count)
            print ds, self.count, delta # DEBUG
            self.end = self.start + delta
            return True
        
        def set_count():
            print 'def set_count()' # DEBUG
            ds = get_divider_sec()
            if not self.end or not ds:
                return False
            self.start = self.start or self.start.now()
            delta = self.end - self.start
            count = int(round(delta.total_seconds() / ds))
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
                if not set_count():
                    self.count = 1
                    if not set_interval():
                        print u'ошибка изменения спецификации'
                        return False
            else:
                if not set_interval():
                    if not set_count():
                        print u'ошибка изменения спецификации'
                        return False
            
        super(Specification, self).save(**kwargs)
    
class DocTemplate(models.Model):
    """ Шаблоны актов и счетов """
    DOCUMENT_CHOICES = (
        ('act', u'Акт'),
        ('invoice', u'Счёт'),
    )
    title = models.CharField(
            max_length=100,
            verbose_name = u"название")
    document = models.CharField(
            max_length=16,
            choices=DOCUMENT_CHOICES,
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
    
class Invoice(models.Model):
    """ Счёт нужен для частичной оплаты заказа"""
    created = models.DateField(
            auto_now_add=True,
            editable=True,
            verbose_name = u"дата")
    user = models.ForeignKey(
            User,
            verbose_name="пользователь")
    is_avance = models.BooleanField(
            default=True,
            verbose_name = u"аванс")
    state = models.IntegerField(
            choices=settings.STATE_INVOICE_CHOICES,
            default=1,
            verbose_name = u"состояние")
    payment = models.IntegerField(
            choices=settings.PAYMENT_INVOICE_CHOICES,
            default=1,
            verbose_name = u"вид расчёта")
    order = models.ForeignKey(
            Order,
            verbose_name = u"заказ")
    date = models.DateField(
            null=True, blank=True,
            verbose_name = u"дата документа")
    summa = models.DecimalField(
            max_digits=10, decimal_places=2,
            default=0.0,
            verbose_name = u"сумма")
    comment = models.TextField(
            blank=True,
            verbose_name = u"комментарий")
    
    
    def __unicode__(self):
        return unicode(self.order)
    
    class Meta:
        ordering = ['user', '-created',]
        verbose_name = u"счёт"
        verbose_name_plural = u"счета"
    
    def save(self, **kwargs):
        other_invoice = self.order.invoice_set.all().exclude(id=self.id)
        payment_invoice = other_invoice.filter(state=settings.STATE_INVOICE_PAYMENT)
        create_invoice = other_invoice.filter(state=settings.STATE_INVOICE_CREATE)
        def payed():
            return sum([x.summa for x in payment_invoice])
        
        if self.state == settings.STATE_INVOICE_PAYMENT:
            self.order.state = settings.STATE_ORDER_CLOSE
            self.order.save()
            if not self.summa:
                self.summa = self.order.summa - payed()
                create_invoice.update(state=settings.STATE_INVOICE_CANCEL)
            elif (self.summa + payed()) >= self.order.summa:
                self.is_avance = False
                create_invoice.update(state=settings.STATE_INVOICE_CANCEL)
                
        super(Invoice, self).save(**kwargs)
    
    @property
    def document(self):
        return u'Счёт на оплату'
    
    @property
    def document_type(self):
        return u'invoice'

class Act(models.Model):
    """ Акт выполненных работ """
    created = models.DateField(
            auto_now_add=True,
            editable=True,
            verbose_name = u"дата")
    user = models.ForeignKey(
            User,
            verbose_name="пользователь")
    order = models.ForeignKey(
            Order,
            verbose_name = u"заказ")
    date = models.DateField(
            null=True, blank=True,
            verbose_name = u"дата документа")
    comment = models.TextField(
            blank=True,
            verbose_name = u"комментарий")
    
    def __unicode__(self):
        return unicode(self.order)
    
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