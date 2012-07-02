# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('barbaris.online.views',
    url(r'^$', 'home', name='home'),
)
