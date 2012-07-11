# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title',)
    #~ fieldsets = (
        #~ (None, {
            #~ 'fields': ('title', 'phones')
        #~ }),
        #~ ('Реквизиты организации', {
            #~ 'classes': ('collapse',),
            #~ 'fields': (('inn','kpp'),'fulltitle','address')
        #~ }),
        #~ ('Банковские реквизиты', {
            #~ 'classes': ('collapse',),
            #~ 'fields': ('bank_bik', 'bank_', 'address')
        #~ }),
    #~ )
admin.site.register(Organization,OrganizationAdmin)

class OrganizationDetailAdmin(admin.ModelAdmin):
    list_display = ('organization', 'id')
admin.site.register(OrganizationDetail,OrganizationDetailAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'id')
    #~ list_filter = ('is_supplier', 'is_client')
    search_fields = ('last_name', 'first_name', 'middle_name', 'organization__title',)
    raw_id_fields = ['organization']
admin.site.register(Client,ClientAdmin)

class ClientDetailAdmin(admin.ModelAdmin):
    list_display = ('client', 'id')
admin.site.register(ClientDetail,ClientDetailAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(Reservation, ReservationAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','id',)
admin.site.register(Category,CategoryAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'id',)
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
    list_display = ('id',)
admin.site.register(Order, OrderAdmin)

class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('price','id',)
    raw_id_fields = ['order','price']
admin.site.register(Specification,SpecificationAdmin)

