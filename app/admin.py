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
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *

class ClientAdmin(admin.ModelAdmin):
    list_display = ('client', 'id',)
admin.site.register(Client, ClientAdmin)

org_append_fieldsets = [
        (u'Реквизиты организации', {
            'classes': ('collapse',),
            'fields': (
                ('inn','kpp', 'ogrn'),
                ('address', 'phones')
                )
        }),
        (u'Банковские реквизиты', {
            'classes': ('collapse',),
            'fields': (
                ('bank_title', 'bank_bik'),
                ('bank_set_account', 'bank_cor_account')
                )
        }),
        (u'Документ', {
            'classes': ('collapse',),
            'fields': (
                ('document_type','document_series', 'document_number'), 
                ('document_date','document_organ', 'document_code')
                )
        }),
    ]

class OrgAdmin(admin.ModelAdmin):
    list_display = ('client', 'fulltitle', 'id')
    search_fields = ('title', 'fulltitle')
    fieldsets = [(None, {
            'fields': (
                'client','title','fulltitle',
                )
        })] + org_append_fieldsets
admin.site.register(Org,OrgAdmin)

class SelfOrgAdmin(admin.ModelAdmin):
    list_display = ('title', 'fulltitle', 'is_active', 'id')
    search_fields = ('title', 'fulltitle')
    fieldsets = [(None, {
            'fields': (
                'is_active', 'title','fulltitle',
                )
        })] + org_append_fieldsets
admin.site.register(SelfOrg, SelfOrgAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('client', 'last_name', 'first_name', 'middle_name', 'sex','id')
    search_fields = ('last_name', 'first_name', 'middle_name', 'org__title',)
    raw_id_fields = ['org']
    fieldsets = (
        (None, {
            'fields': (
                'client',
                ('last_name', 'first_name', 'middle_name', 'sex',), 
                )
        }),
        (u'Место рождения', {
            'classes': ('collapse',),
            'fields': (
                'birth_day',
                ('birth_country','birth_region', 'birth_sity'),
                ('birth_area', 'birth_settlement'),
                )
        }),
        (u'Место жительства', {
            'classes': ('collapse',),
            'fields': (
                'residence_sitizenship',
                ('residence_country', 'residence_region','residence_sity',),
                ('residence_area', 'residence_settlement'),
                'residence_street',
                ('residence_house', 'residence_case', 'residence_apartment'),
                )
        }),
        (u'Документ', {
            'classes': ('collapse',),
            'fields': (
                ('document_type','document_series', 'document_number'), 
                ('document_date','document_organ', 'document_code')
                )
        }),
    )
admin.site.register(Person,PersonAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('title','id',)
admin.site.register(Reservation, ReservationAdmin)

#~ class CategoryAdmin(admin.ModelAdmin):
    #~ list_display = ('title','id',)
#~ admin.site.register(Category,CategoryAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'prices', 'id',)
    list_filter = ('category',)
admin.site.register(Service, ServiceAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('num', 'service', 'prices', 'id',)
    list_filter = ('service',)
admin.site.register(Room, RoomAdmin)

class PriceAdmin(admin.ModelAdmin):
    list_display = ('service', 'start_date','price','divider', 'is_active','id',)
    list_filter = ('service__category', 'is_active', 'start_date')
    raw_id_fields = ['service']
admin.site.register(Price, PriceAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'created', 'updated', 'state')
    list_filter = ('state', 'user',)
    filter_horizontal = (
        #~ 'payment_clients', 
        'clients',
    )
    fieldsets = (
        (None, {
            'fields': (
                (u'user', u'state', u'is_divdoc'),
                u'clients',
            )
        }),
        (u'Дополнительно', {
            u'classes': ('collapse',),
            u'fields': (
                u'comment',
            )
        }),
    )
admin.site.register(Order, OrderAdmin)

class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('price', 'order', 'summa', 'id',)
    list_filter = ('price__service__category', 'reservation')
    raw_id_fields = ['order','price']
    search_fields = ('id',)
admin.site.register(Specification,SpecificationAdmin)

class DocTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'document', 'is_default','id',)
    list_filter = ('document', 'is_default')
admin.site.register(DocTemplate, DocTemplateAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'order', 'client', 'date','id',)
    list_filter = ('state', 'user')
    raw_id_fields = ['order','client']
    search_fields = ('id',)
admin.site.register(Invoice, InvoiceAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'invoice', 'created', 'updated')
    list_filter = ('user', 'payment')
    raw_id_fields = ['invoice']
    search_fields = ('id',)
admin.site.register(Payment, PaymentAdmin)

class ActAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'order', 'client', 'date',)
    list_filter = ('user',)
    raw_id_fields = ['order','client','invoice']
    search_fields = ('id',)
admin.site.register(Act, ActAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'user','id',)
    list_filter = ('user',)
    search_fields = ('text', )
admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'question', 'id',)
    list_filter = ('user',)
    search_fields = ('text', 'question')
    raw_id_fields = ['question']
admin.site.register(Answer, AnswerAdmin)
