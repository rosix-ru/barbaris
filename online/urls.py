# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('barbaris.online.views',
    url(r'^$', 'monitor', name='monitor'),
    url(r'^orders/$', 'orders', name='orders'),
    url(r'^pricelist/$', 'pricelist', name='pricelist'),
    url(r'^invoices/$', 'invoices', name='invoices'),
    url(r'^acts/$', 'acts', name='acts'),
    url(r'^clients/$', 'clients', name='clients'),
    url(r'^analyze/$', 'analyze', name='analyze'),
    url(r'^reports/$', 'reports', name='reports'),
    url(r'^questions/$', 'questions', name='questions'),
)
