from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

urlpatterns = patterns('main.views',
               url(r'^$', 'home', name='home'),
               url(r'^panel/(?P<pk>\d+)/$', 'panel', name='panel'),
               url(r'^reports/(?P<pk>\d+)/$', 'reports', name='reports'),               
               url(r'^accidents/(?P<pk>\d+)/$', 'accidents', name='accidents'),
               url(r'^requeriment/(?P<pk>\d+)/$', 'requeriment', name='requeriment'),
               url(r'^agreement/$', 'agreement', name = 'agreement'),
               url(r'^company/new$', 'new_company', name = 'new_company'),   
               url(r'^calendar/(?P<pk>\d+)/$', 'calendar', name='calendar'),
               url(r'^law/$', 'law', name='law'),   

           )
