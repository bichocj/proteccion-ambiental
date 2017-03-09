from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from proteccion_ambiental import settings

urlpatterns = patterns('main.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^configuration/requirement-list/$', 'config_requirements_list', name='config_requirements_list'),
                       url(r'^configuration/requirement-new/$', 'config_requirement_new', name='config_requirement_new'),
                       url(r'^(?P<company_slug>[-\w]+)/requirements/requirement-new/$', 'requirement_new', name='requirement_new'),
                       url(r'^(?P<company_slug>[-\w]+)/panel/$', 'panel', name='panel'),
                       url(r'^(?P<company_slug>[-\w]+)/configuration/$', 'configuration', name='configuration'),
                       url(r'^(?P<company_slug>[-\w]+)/reports/$', 'reports', name='reports'),
                       url(r'^(?P<company_slug>[-\w]+)/accident-list/$', 'accident_list', name='accident_list'),
                       url(r'^(?P<company_slug>[-\w]+)/accident-edit/(?P<accident_pk>\d+)/$', 'accident_edit',
                           name='accident_edit'),
                       url(r'^(?P<company_slug>[-\w]+)/accident-new/$', 'accident_new', name='accident_new'),
                       url(r'^(?P<company_slug>[-\w]+)/accident-delete/(?P<accident_pk>\d+)/$', 'accident_delete',
                           name='accident_delete'),
                       url(r'^(?P<company_slug>[-\w]+)/requirements/$', 'requirements_list', name='requirements_list'),
                       url(r'^(?P<company_slug>[-\w]+)/requirements/formats/(?P<requirement_pk>\d+)/$', 'format_list',
                           name='format_list'),
                       url(r'^(?P<company_slug>[-\w]+)/requirements/formats/new_pdf/(?P<requirement_pk>\d+)/$',
                           'format_new_pdf',
                           name='format_new_pdf'),
                       url(r'^(?P<company_slug>[-\w]+)/requirements/formats/new_other/(?P<requirement_pk>\d+)/$',
                           'format_new_other',
                           name='format_new_other'),
                       url(r'^(?P<company_slug>[-\w]+)/agreement/$', 'agreement', name='agreement'),
                       url(r'^company-new/$', 'company_new', name='company_new'),
                       url(r'^company-list/$', 'company_list', name='company_list'),

                       )
urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                        )
