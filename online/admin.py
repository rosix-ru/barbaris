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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title',)
admin.site.register(Organization,OrganizationAdmin)

class OrganizationDetailAdmin(admin.ModelAdmin):
    list_display = ('organization', 'is_active', 'id')
    fieldsets = (
        (None, {
            'fields': (
                ('organization', 'is_active'), 
                'fulltitle',
                )
        }),
        (u'Реквизиты организации', {
            'classes': ('collapse',),
            'fields': (
                ('inn','kpp', 'ogrn'),
                ('address', 'phones')
                )
        }),
        (u'Документ', {
            'classes': ('collapse',),
            'fields': (
                ('document_type','document_series', 'document_number'), 
                ('document_date','document_organ', 'document_code')
                )
        }),
        (u'Банковские реквизиты', {
            'classes': ('collapse',),
            'fields': (
                ('bank_title', 'bank_bik'),
                ('bank_set_account', 'bank_cor_account')
                )
        }),
    )
admin.site.register(OrganizationDetail,OrganizationDetailAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'id')
    #~ list_filter = ('is_supplier', 'is_client')
    search_fields = ('last_name', 'first_name', 'middle_name', 'organization__title',)
    raw_id_fields = ['organization']
admin.site.register(Client,ClientAdmin)

class ClientDetailAdmin(admin.ModelAdmin):
    list_display = ('client', 'is_active', 'id')
    fieldsets = (
        (None, {
            'fields': (
                ('client', 'is_active'), 
                'sex',
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
        (u'Документ', {
            'classes': ('collapse',),
            'fields': (
                ('document_type','document_series', 'document_number'), 
                ('document_date','document_organ', 'document_code')
                )
        }),
        (u'Место жительства', {
            'classes': ('collapse',),
            'fields': (
                'sitizenship',
                ('residence_country', 'residence_region','residence_sity',),
                ('residence_area', 'residence_settlement'),
                'residence_street',
                ('residence_house', 'residence_case', 'residence_apartment'),
                )
        }),
    )
admin.site.register(ClientDetail,ClientDetailAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('title','id',)
admin.site.register(Reservation, ReservationAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','id',)
admin.site.register(Category,CategoryAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'prices', 'id',)
    list_filter = ('category',)
admin.site.register(Service, ServiceAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('num', 'service', 'price', 'id',)
    list_filter = ('service',)
admin.site.register(Room, RoomAdmin)

class PriceAdmin(admin.ModelAdmin):
    list_display = ('service', 'start_date','price','divider', 'is_active','id',)
    list_filter = ('service__category', 'is_active', 'start_date')
    raw_id_fields = ['service']
admin.site.register(Price, PriceAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'updated', 'state','id',)
    list_filter = ('state', 'user',)
    filter_horizontal = ('other_clients', 'attributes')
    fieldsets = (
        (None, {
            'fields': (
                ('client'), 
                ('user', 'state'), 
                )
        }),
        (u'Дополнительно', {
            'classes': ('collapse',),
            'fields': (
                'other_clients','attributes', 'comment',
                )
        }),
    )
admin.site.register(Order, OrderAdmin)

class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('price', 'order', 'summa', 'id',)
    list_filter = ('price__service__category', 'reservation')
    raw_id_fields = ['order','price']
admin.site.register(Specification,SpecificationAdmin)

