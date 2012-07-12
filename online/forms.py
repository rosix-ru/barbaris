# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from barbaris.online import models

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        exclude = ('is_seller',)

class OrganizationDetailForm(forms.ModelForm):
    class Meta:
        model = models.OrganizationDetail
        exclude = ('is_active',)
        widgets = {
            'fulltitle': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client

class ClientDetailForm(forms.ModelForm):
    class Meta:
        model = models.ClientDetail
        exclude = ('is_active',)

class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        exclude = ('created','updated', 'state')

class SpecificationForm(forms.ModelForm):
    class Meta:
        model = models.Specification
        exclude = ('created','updated', )
