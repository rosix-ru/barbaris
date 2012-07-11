# -*- coding: utf-8 -*-
from django.db import models, connection, transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from barbaris.online.managers import ActivePriceManager,\
    CreateOrderManager, ReservOrderManager, AcceptOrderManager,\
    AvanseOrderManager, PaymentOrderManager, CancelOrderManager,\
    WorkOrderManager,\
    SellerOrganizationManager, BuyerOrganizationManager,\
    PrivateClientManager

import datetime

class Organization(models.Model):
    """ Представляет собственную организацию-продавца услуг(seller),
        либо покупателя.
    """
    is_seller = models.BooleanField(
            default=False,
            verbose_name = "продавец")
    title = models.CharField(
            max_length=100,
            verbose_name = "название")
    
    objects = models.Manager()
    sellers = SellerOrganizationManager()
    buyers  = BuyerOrganizationManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = "организацию"
        verbose_name_plural = "организации"

class OrganizationDetail(models.Model):
    """ Расширенная информация об организации """
    organization = models.OneToOneField(
            Organization,
            verbose_name = "организация")
    fulltitle = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = "полное название")
    inn = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "ИНН")
    kpp = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "КПП")
    ogrn = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "ОГРН")
    address = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = "адрес")
    phones = models.CharField(
            max_length=100,
            blank=True,
            verbose_name = "телефоны")
    # Поля документа организации
    document_type = models.CharField(
            max_length=50,
            blank=True,
            verbose_name = "тип")
    document_series = models.CharField(
            max_length=10,
            blank=True,
            verbose_name = "серия")
    document_number = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "номер")
    document_date = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "дата выдачи")
    document_organ = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = "орган выдачи")
    document_code = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "код органа")
    # Банковские реквизиты
    bank_bik = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "БИК")
    bank_title = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = "название")
    bank_set_account = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = "Р/СЧ")
    bank_cor_account = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = "КОР/СЧ")
    
    def __unicode__(self):
        return unicode(self.organization)
        
    class Meta:
        ordering = ['organization',]
        verbose_name = "карточку организации"
        verbose_name_plural = "карточки организаций"

class Client(models.Model):
    """ Клиент - физическое лицо, либо представитель фирмы, 
        который может быть представлен существительным во 
        множественном числе, например: "нефтяники", в 
        обязательном поле last_name.
    """
    organization = models.ForeignKey(
            Organization,
            null=True, blank=True,
            verbose_name = "организация")
    last_name = models.CharField(
            max_length=50,
            verbose_name = "фамилия")
    first_name = models.CharField(
            max_length=50,
            blank=True,
            verbose_name = "имя")
    middle_name = models.CharField(
            max_length=50,
            blank=True,
            verbose_name = "отчество")
    phones = models.CharField(
            max_length=50,
            blank=True,
            verbose_name = "телефоны")
    
    objects = models.Manager()
    privates = PrivateClientManager()
    
    def __unicode__(self):
        fio = u' '.join(
                [self.last_name, self.first_name, self.middle_name]
                ).replace("  ", ' ')
        return fio
        
    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']
        verbose_name = "клиента"
        verbose_name_plural = "клиенты"

class ClientDetail(models.Model):
    """ Расширенная информация о клиенте """
    SEX_CHOICES = (
        ('муж','мужской'),
        ('жен','женский')
    )
    DOCUMENT_CHOICES = (
        ('паспорт','паспорт'),
        ('водительское','водительское удостоверение')
    )
    client = models.OneToOneField(
            Client,
            verbose_name = "клиент")
    sex = models.CharField(
            max_length=3,
            choices=SEX_CHOICES,
            blank=True,
            verbose_name = "пол")
    sitizenship = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = 'гражданство')
    # Поля места рождения
    birth_day = models.DateField(
            null=True, blank=True,
            verbose_name = 'дата')
    birth_country = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = 'страна')
    birth_region = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = 'регион')
    birth_area = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = 'район')
    birth_sity = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = 'город')
    birth_settlement = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = 'населённый пункт')
    # Поля документа клиента
    document_type = models.CharField(
            max_length=16,
            choices=DOCUMENT_CHOICES,
            blank=True,
            verbose_name = "тип")
    document_series = models.CharField(
            max_length=10,
            blank=True,
            verbose_name = "серия")
    document_number = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "номер")
    document_date = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "дата выдачи")
    document_organ = models.CharField(
            max_length=255,
            blank=True,
            verbose_name = "орган выдачи")
    document_code = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = "код органа")
    # Поля места жительства
    residence_country = models.CharField(
            max_length=16,
            blank=True,
            verbose_name = 'страна')
    residence_region = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = 'регион')
    residence_area = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = 'район')
    residence_sity = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = 'город')
    residence_settlement = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = 'населённый пункт')
    residence_street = models.CharField(
            max_length=32,
            blank=True,
            verbose_name = 'улица')
    residence_house = models.CharField(
            max_length=8,
            blank=True,
            verbose_name = 'дом')
    residence_case = models.CharField(
            max_length=8,
            blank=True,
            verbose_name = 'корпус')
    residence_apartment = models.CharField(
            max_length=8,
            blank=True,
            verbose_name = 'квартира')
    
    def __unicode__(self):
        return unicode(self.client)
        
    class Meta:
        ordering = ['client',]
        verbose_name = "карточку клиента"
        verbose_name_plural = "карточки клиентов"

class Category(models.Model):
    """ Категория услуги """
    title = models.CharField(
            max_length=255,
            verbose_name = "название")
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name = "категорию"
        verbose_name_plural = "категории"

class Service(models.Model):
    """ Услуга """
    category = models.ForeignKey(
            Category,
            verbose_name = "категория")
    title = models.CharField(
            max_length=255,
            verbose_name = "название")
    is_rooms = models.BooleanField(
            default=False,
            verbose_name = "подразделяется на номера")
    is_reserved = models.BooleanField(
            default=False,
            verbose_name = "разрешить бронирование")
    
    def __unicode__(self):
        return '%s: %s' % (unicode(self.category), self.title)
        
    class Meta:
        ordering = ['title']
        verbose_name = "услугу"
        verbose_name_plural = "услуги"
    
    @property
    def price(self):
        prices = Price.actives.filter(service=self)
        return '; '.join([ 
            p.get_divider_display() +'='+ str(round(p.price, 2))
            for p in prices
            ])

class Room(models.Model):
    """ Гостиничные номера """
    service = models.ForeignKey(
            Service,
            limit_choices_to={'is_rooms': True},
            verbose_name = "тип номера")
    num = models.IntegerField(
            unique=True,
            verbose_name = "номер")
    
    def __unicode__(self):
        return str(self.num)
        
    class Meta:
        ordering = ['service', 'num']
        verbose_name = "номер"
        verbose_name_plural = "номера"
    
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
            verbose_name = "услуга")
    price = models.DecimalField(
            max_digits=10, decimal_places=2,
            default=0.0,
            verbose_name = "цена")
    start_date = models.DateField(
            default=datetime.date.today() + datetime.timedelta(1),
            verbose_name = "начало действия")
    divider = models.IntegerField(
            choices=settings.PRICE_DIVIDER_CHOICES,
            default=settings.DAY_PRICE,
            verbose_name = "делитель")
    
    objects = models.Manager()
    actives = ActivePriceManager()
    
    def __unicode__(self):
        return unicode(self.service)
    
    class Meta:
        ordering = ['service__category__title','service','start_date',]
        verbose_name = "цену"
        verbose_name_plural = "цены"
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
            verbose_name = "название")
    expired_days = models.IntegerField(
            default=0,
            verbose_name = "истечение в днях")
    percent = models.DecimalField(
            max_digits=3, decimal_places=2,
            verbose_name = "процент надбавки",
            help_text='"10%" это "0.10"')
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = "вид бронирования"
        verbose_name_plural = "виды бронирования"
    
class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(
            User,
            verbose_name="пользователь")
    state = models.IntegerField(
            choices=settings.ORDER_STATE_CHOICES,
            default=1,
            verbose_name="состояние")
    client = models.ForeignKey(
            Client,
            verbose_name="клиент")
    start_date = models.DateField(
            null=True, blank=True,
            verbose_name = "дата начала")
    start_time = models.TimeField(
            null=True, blank=True,
            verbose_name = "время начала")
    end_date = models.DateField(
            null=True, blank=True,
            verbose_name = "дата окончания")
    end_time = models.TimeField(
            null=True, blank=True,
            verbose_name = "время окончания")
    comment = models.CharField(
            max_length=255,
            blank=True,
            verbose_name="комментарий")
    card = models.BooleanField(
            default=False,
            verbose_name = "оплата по карте")
    
    
    objects  = models.Manager()
    creates  = CreateOrderManager()
    accepts  = AcceptOrderManager()
    avances  = AvanseOrderManager()
    payments = PaymentOrderManager()
    cancels  = CancelOrderManager()
    workeds  = WorkOrderManager()
    
    def __unicode__(self):
        return unicode(self.client)
    
    class Meta:
        ordering = ['-updated', 'client']
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        get_latest_by = 'updated'
    
    @property
    def summa(self):
        return sum([ x.summa for x in self.specification_set.all() ])
    
class Specification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    order = models.ForeignKey(
            Order,
            verbose_name="заказ")
    price = models.ForeignKey(
            Price,
            verbose_name="цена")
    quantity = models.IntegerField(
            default=0,
            verbose_name="количество")
    start_date = models.DateField(
            null=True, blank=True,
            verbose_name = "дата начала")
    start_time = models.TimeField(
            null=True, blank=True,
            verbose_name = "время начала")
    end_date = models.DateField(
            null=True, blank=True,
            verbose_name = "дата окончания")
    end_time = models.TimeField(
            null=True, blank=True,
            verbose_name = "время окончания")
    reservation = models.ForeignKey(
            Reservation,
            null=True, blank=True,
            verbose_name="вид бронирования")
            
    def __unicode__(self):
        return unicode(self.price)
    
    class Meta:
        ordering = ['order', '-updated',]
        verbose_name = "спецификацию"
        verbose_name_plural = "спецификации"
    
    @property
    def summa(self):
        if self.reservation and self.price.service.is_reserved:
            markup = self.price.price*self.order.reservation.percent
        else:
            markup = 0
        return round(self.price.price*self.quantity+markup, 2)
    
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
