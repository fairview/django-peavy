from django.conf import settings
from django.conf.urls.defaults import include, patterns, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'peavy_demo.views.home', name='home'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    (r'^peavy/', include('peavy.urls', namespace='peavy')),
)

if 'devserver' == getattr(settings, 'APP_SERVER', None):
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
