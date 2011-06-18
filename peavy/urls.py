from django.conf.urls.defaults import *

urlpatterns = patterns('peavy.views',
    url(r'^$', 'dashboard', name='peavy_dashboard'),
    url(r'^debug/(?P<record_id>[^/]+)/$', 'debug_page', name='peavy_debug_page'),
)

