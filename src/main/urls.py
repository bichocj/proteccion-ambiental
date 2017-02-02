from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

urlpatterns = patterns('main.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^panel/(?P<company_pk>\d+)/$', 'panel', name='panel'),
                       url(r'^reports/(?P<company_pk>\d+)/$', 'reports', name='reports'),
                       url(r'^accident-list/(?P<company_pk>\d+)/$', 'accident_list', name='accident_list'),
                       url(r'^accident-new/(?P<company_pk>\d+)/$', 'accident_new', name='accident_new'),
                       url(r'^requirements/(?P<company_pk>\d+)/$', 'requirements_list', name='requirements_list'),
                       url(r'^requirements/formats/(?P<requirement_pk>\d+)/$', 'format_list', name='format_list'),
                       url(r'^agreement/$', 'agreement', name='agreement'),
                       url(r'^company-new/$', 'company_new', name='company_new'),
                       url(r'^company-list/$', 'company_list', name='company_list'),
                       )
