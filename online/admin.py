# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'inn', 'address', 'id')
    search_fields = ('title', 'inn')
admin.site.register(Organization,OrganizationAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'birth', 'is_client', 'id')
    list_filter = ('is_supplier', 'is_client')
    search_fields = ('title', 'inn')
    filter_horizontal = ['users', ]
admin.site.register(Client,ClientAdmin)
