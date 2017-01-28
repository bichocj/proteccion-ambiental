from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

urlpatterns = patterns('main.views',
               url(r'^$', 'home', name='home'),
               url(r'^panel/(?P<pk>\d+)/$', 'panel', name='panel'),
               url(r'^reports/(?P<pk>\d+)/$', 'reports', name='reports'),
               url(r'^accidents/(?P<pk>\d+)/$', 'accidents', name='accidents'),
               url(r'^requerimientos/(?P<pk>\d+)/$', 'requirements_list', name='requirements_list'),
               url(r'^formats/(?P<pk>\d+)/$', 'format_list', name='format_list'),
               url(r'^agreement/$', 'agreement', name = 'agreement'),
               url(r'^company/new/$', 'new_company', name = 'new_company'),
               url(r'^calendar/service/(?P<pk>\d+)/$', 'calendar_service', name='calendar_service'),
               url(r'^calendar/training/(?P<pk>\d+)/$', 'calendar_training', name='calendar_training'),
               url(r'^law/$', 'law', name='law'),

           )
