# -*- coding: utf-8 -*-
from django.db import models, connection, transaction
from django.db.models.aggregates import Sum
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

import datetime

#~ class Client(models.Model):
    #~ 
    #~ title = models.CharField(
            #~ max_length=255,
            #~ verbose_name = _('title'))
    #~ short_title = models.CharField(
            #~ max_length=16,
            #~ blank=True,
            #~ verbose_name = _('short title'))
    #~ inn = models.CharField(
            #~ max_length=16,
            #~ unique=True,
            #~ verbose_name=_('INN'))
    #~ address = models.CharField(
            #~ max_length=255,
            #~ blank=True,
            #~ verbose_name=_('address'))
    #~ 
    #~ def __unicode__(self):
        #~ return self.title
        #~ 
    #~ class Meta:
        #~ ordering = ['title']
        #~ verbose_name = _('client')
        #~ verbose_name_plural = _('clients')
