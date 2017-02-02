from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from proteccion_ambiental import settings

urlpatterns = patterns('main.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^panel/(?P<company_pk>\d+)/$', 'panel', name='panel'),
                       url(r'^reports/(?P<company_pk>\d+)/$', 'reports', name='reports'),
                       url(r'^accident-list/(?P<company_pk>\d+)/$', 'accident_list', name='accident_list'),
                       url(r'^accident-edit/(?P<accident_pk>\d+)/$', 'accident_edit', name='accident_edit'),
                       url(r'^accident-new/(?P<company_pk>\d+)/$', 'accident_new', name='accident_new'),
                       url(r'^accident-delete/(?P<accident_pk>\d+)/$', 'accident_delete', name='accident_delete'),
                       url(r'^requirements/(?P<company_pk>\d+)/$', 'requirements_list', name='requirements_list'),
                       url(r'^requirements/formats/(?P<requirement_pk>\d+)/$', 'format_list', name='format_list'),
                       url(r'^agreement/$', 'agreement', name='agreement'),
                       url(r'^company/new/$', 'new_company', name='new_company'),
                       url(r'^law/$', 'law', name='law'),

                       )
urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                        )
