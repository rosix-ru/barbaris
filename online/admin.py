# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'inn', 'address', 'id')
    search_fields = ('title', 'inn')
admin.site.register(Organization,OrganizationAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'birth', 'id')
    #~ list_filter = ('is_supplier', 'is_client')
    search_fields = ('last_name', 'first_name', 'middle_name', 'organization__title', 'organization__inn')
admin.site.register(Client,ClientAdmin)
