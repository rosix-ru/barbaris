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

from django import forms
from django.utils.translation import ugettext_lazy as _
import models

class OrgForm(forms.ModelForm):
    class Meta:
        model = models.Org
        exclude = ('is_seller',)

class OrgDetailForm(forms.ModelForm):
    class Meta:
        model = models.OrgDetail
        fields = ('fulltitle', 'inn', 'kpp', 'ogrn', 'address', 'phones')
        widgets = {
            'fulltitle': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }

class OrgBankForm(forms.ModelForm):
    class Meta:
        model = models.OrgDetail
        fields = ('bank_bik', 'bank_title', 'bank_set_account', 
            'bank_cor_account')
        widgets = {
            'bank_title': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }

class OrgDocumentForm(forms.ModelForm):
    class Meta:
        model = models.OrgDetail
        fields = ('document_type', 'document_series', 
            'document_number', 'document_date', 'document_organ', 
            'document_code')
        widgets = {
            'document_date': forms.TextInput(attrs={'data-toggle': 'datepicker'}),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = models.Person

class PersonResidenceForm(forms.ModelForm):
    class Meta:
        model = models.PersonDetail
        fields = ('residence_sitizenship', 'residence_country', 
            'residence_region', 'residence_area', 'residence_sity',
            'residence_settlement', 'residence_street',
            'residence_house', 'residence_case', 'residence_apartment')

class PersonBirthForm(forms.ModelForm):
    class Meta:
        model = models.PersonDetail
        fields = ('birth_day', 'birth_country', 'birth_area', 
            'birth_sity', 'birth_settlement',)
        widgets = {
            'birth_day': forms.TextInput(attrs={'data-toggle': 'datepicker'}),
        }

class PersonDocumentForm(forms.ModelForm):
    class Meta:
        model = models.PersonDetail
        fields = ('document_type', 'document_series', 
            'document_number', 'document_date', 'document_organ', 
            'document_code')
        widgets = {
            'document_date': forms.TextInput(attrs={'data-toggle': 'datepicker'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        exclude = ('created','updated', 'state', 'user')

class SpecificationForm(forms.ModelForm):
    class Meta:
        model = models.Specification
        exclude = ('created','updated', 'order' )
        widgets = {
            'start': forms.TextInput(attrs={'data-toggle': 'datetimepicker'}),
            'end':  forms.TextInput(attrs={'data-toggle': 'datetimepicker'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = models.Invoice
        exclude = ('created', 'order', 'user', 'state' )
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
            'date':  forms.TextInput(attrs={'data-toggle': 'datepicker'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = models.Payment
        exclude = ('created', 'updated', 'user', 'invoice' )
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
        }

class ActForm(forms.ModelForm):
    class Meta:
        model = models.Act
        exclude = ('created', 'order', 'user', 'state' )
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
            'date':  forms.TextInput(attrs={'data-toggle': 'datepicker'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        exclude = ('created', 'user', )
        widgets = {
            'theme':  forms.TextInput(attrs={'class': 'span12'}),
            'text': forms.Textarea(attrs={'class': 'span12', 'rows': 2}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        exclude = ('created', 'user', 'question' )
        widgets = {
            'text': forms.Textarea(attrs={'class': 'span12', 'rows': 2}),
        }
