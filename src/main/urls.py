from django.conf.urls import url, include
from django.views.static import serve

import main._views.personal
import main._views.report
from main import views
from main.api import router
from proteccion_ambiental import settings

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^config/indices-list/$', views.config_indices_list, name='config_indices_list'),

    url(r'^config/requirement-list/$', views.config_requirements_list, name='config_requirements_list'),
    url(r'^config/requirement-new/$', views.config_requirement_new, name='config_requirement_new'),

    url(r'^config/requirement/(?P<requirement_pk>\d+)/formats/$', views.config_requirement_format_list,
        name='config_requirement_format_list'),
    url(r'^config/requirement/(?P<requirement_pk>\d+)/format/new/$', views.config_requirement_format_new,
        name='config_requirement_format_new'),
    url(r'^config/requirement/(?P<requirement_pk>\d+)/format/(?P<format_pk>\d+)/update/$',
        views.config_requirement_format_update, name='config_requirement_format_update'),

    url(r'^company-new/$', views.company_new, name='company_new'),
    url(r'^company-list/$', views.company_list, name='company_list'),
    url(r'^company-edit/(?P<company_slug>[-\w]+)/$', views.company_edit, name='company_edit'),

    url(r'^(?P<company_slug>[-\w]+)/medic_exams/$', views.medic_exam, name='medic_exam'),
    url(r'^(?P<company_slug>[-\w]+)/medic_exams/new/$', views.medic_exam_new,
        name='medic_exam_new'),
    url(r'^(?P<company_slug>[-\w]+)/medic_exams/(?P<medic_pk>\d+)/edit/$', views.medic_exam_edit,
        name='medic_exam_edit'),
    url(r'^(?P<company_slug>[-\w]+)/medic_exams/(?P<medic_pk>\d+)/delete/$',
        views.medic_exam_delete, name='medic_exam_delete'),

    url(r'^(?P<company_slug>[-\w]+)/workers/$', views.workers, name='workers'),
    url(r'^(?P<company_slug>[-\w]+)/workers/new/$', views.worker_new,
        name='worker_new'),
    url(r'^(?P<company_slug>[-\w]+)/workers/(?P<worker_pk>\d+)/edit/$', views.worker_edit,
        name='worker_edit'),
    url(r'^(?P<company_slug>[-\w]+)/workers/(?P<worker_pk>\d+)/record/$', views.worker_record,
        name='worker_record'),
    url(r'^(?P<company_slug>[-\w]+)/workers/(?P<worker_pk>\d+)/delete/$',
        views.worker_delete, name='worker_delete'),

    url(r'^(?P<company_slug>[-\w]+)/requisitos_legales/$', views.legal_requirement, name='legal_requirement'),
    url(r'^(?P<company_slug>[-\w]+)/requisitos_legales/new/$', views.legal_requirement_new,
        name='legal_requirement_new'),
    url(r'^(?P<company_slug>[-\w]+)/requisitos_legales/(?P<requirement_pk>\d+)/edit/$', views.legal_requirement_edit,
        name='legal_requirement_edit'),
    url(r'^(?P<company_slug>[-\w]+)/requisitos_legales/(?P<requirement_pk>\d+)/delete/$',
        views.legal_requirement_delete, name='legal_requirement_delete'),

    url(r'^(?P<company_slug>[-\w]+)/panel/$', views.panel, name='panel'),
    url(r'^(?P<company_slug>[-\w]+)/requirements/$', views.requirements_list, name='requirements_list'),
    url(r'^(?P<company_slug>[-\w]+)/requirements/new/$', views.requirement_new, name='requirement_new'),
    url(r'^(?P<company_slug>[-\w]+)/requirements/edit/(?P<requirement_pk>\d+)/$', views.requirement_edit,
        name='requirement_edit'),
    url(r'^(?P<company_slug>[-\w]+)/requirement/(?P<requirement_pk>\d+)/formats/$', views.format_list,
        name='format_list'),

    url(r'^(?P<company_slug>[-\w]+)/requirement/(?P<requirement_pk>\d+)/format/(?P<format_pk>\d+)/update/',
        views.format_update, name='format_update'),
    url(r'^(?P<company_slug>[-\w]+)/requirement/(?P<requirement_pk>\d+)/format/new/$', views.format_new,
        name='format_new'),

    url(r'^(?P<company_slug>[-\w]+)/config/$', views.config, name='config'),

    url(r'^(?P<company_slug>[-\w]+)/accident-list/$', views.accident_list, name='accident_list'),
    url(r'^(?P<company_slug>[-\w]+)/accident-edit/(?P<accident_pk>\d+)/$', views.accident_edit, name='accident_edit'),
    url(r'^(?P<company_slug>[-\w]+)/accident-new/$', views.accident_new, name='accident_new'),
    url(r'^(?P<company_slug>[-\w]+)/accident-delete/(?P<accident_pk>\d+)/$', views.accident_delete,
        name='accident_delete'),
    url(r'^(?P<company_slug>[-\w]+)/agreement/$', views.agreement, name='agreement'),

]

# Users
urlpatterns += [
    url(r'^(?P<company_slug>[-\w]+)/user/new/$', views.user_new, name='user_new'),
    url(r'^(?P<company_slug>[-\w]+)/user/delete/(?P<pk>\d+)/$', views.user_delete, name='user_delete'),
    # url(r'^(?P<company_slug>[-\w]+)/user/edit/(?P<pk>\d+)/$', views.user_edit, name='user_edit'),
]

# Personal
urlpatterns += [
    url(r'^(?P<company_slug>[-\w]+)/personal/contador/$', main._views.personal.personal_counter_list,
        name='personal_counter_list'),
    url(r'^(?P<company_slug>[-\w]+)/personal/contador/(?P<counter_pk>\d+)/edit/$',
        main._views.personal.personal_counter_edit, name='personal_counter_edit'),
]

# Reports
urlpatterns += [
    # Reportes
    url(r'^(?P<company_slug>[-\w]+)/informes/$', main._views.report.reports, name='reports'),
    url(r'^(?P<company_slug>[-\w]+)/informe/resumen/$', main._views.report.report_resume, name='reports_resume'),
    url(r'^(?P<company_slug>[-\w]+)/informe/resumen/data/(?P<key>[-\w]+)/$', main._views.report.report_resume_data, name='report_resume_data'),
    url(r'^(?P<company_slug>[-\w]+)/informe/mensual/(?P<month>\d+)/$', main._views.report.monthly_report, name='report_monthly'),
    url(r'^(?P<company_slug>[-\w]+)/informe/mensual/actualizar/(?P<month>\d+)/$', main._views.report.refresh_inform, name='report_update'),
    # Indices
    url(r'^(?P<company_slug>[-\w]+)/indices/$', views.indices, name='indices'),
    # url(r'^(?P<company_slug>[-\w]+)/indices/restore/(?P<mounth>\d+)/$', views.restore_indices, name='restore_indices'),
    # url(r'^(?P<company_slug>[-\w]+)/indices/(?P<indice_slug>[-\w]+)/$', views.indices_update, name='indices_update'),

]

# API
urlpatterns += [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
