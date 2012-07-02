# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import redirect
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

def homeredirect(request):
    return redirect('/')

urlpatterns = patterns('',
    url(r'^$', 'barbaris.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^accounts/login/$', 'login', name="login"),
    url(r'^accounts/logout/$', 'logout', name="logout"),
    url(r'^accounts/profile/$', homeredirect, name="profile"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    )
