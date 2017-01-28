from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

urlpatterns = patterns('main.views',
               url(r'^$', 'home', name='home'),
               url(r'^panel/(?P<pk>\d+)/$', 'panel', name='panel'),
               url(r'^reports/(?P<pk>\d+)/$', 'reports', name='reports'),
               url(r'^accidents/(?P<pk>\d+)/$', 'accidents', name='accidents'),
               url(r'^requerimientos/(?P<pk>\d+)/$', 'requirements_list', name='requirements_list'),
               url(r'^requerimientos/formats/(?P<pk>\d+)/$', 'format_list', name='format_list'),
               url(r'^agreement/$', 'agreement', name = 'agreement'),
               url(r'^company/new/$', 'new_company', name = 'new_company'),
               url(r'^law/$', 'law', name='law'),

           )
