from django.conf.urls.defaults import *

urlpatterns = patterns('peavy.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^debug/(?P<record_id>[^/]+)/$', 'debug_page', name='debug_page'),
)

