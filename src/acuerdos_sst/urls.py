from django.conf.urls import url

from acuerdos_sst import views

urlpatterns = [
    url(r'^(?P<company_slug>[-\w]+)/$', views.home, name="home"),
    url(r'^(?P<company_slug>[-\w]+)/list/$', views.agreement_list, name="agreement_list"),
    url(r'^(?P<company_slug>[-\w]+)/new/$', views.agreement_new, name="agreement_new"),
    url(r'^(?P<company_slug>[-\w]+)/desactivar/(?P<agreement_pk>\d+)/$', views.desactive_agreement,
        name="desactive_agreement"),
    url(r'^(?P<company_slug>[-\w]+)/edit/(?P<agreement_pk>\d+)/$', views.agreement_edit, name="agreement_edit"),
    url(r'^(?P<company_slug>[-\w]+)/delete/(?P<agreement_pk>\d+)/$', views.agreement_delete, name="agreement_delete"),
    url(r'^(?P<company_slug>[-\w]+)/detalis/(?P<agreement_pk>\d+)/$', views.agreement_detail, name="agreement_detail"),
    url(r'^(?P<company_slug>[-\w]+)/detalis/(?P<agreement_pk>\d+)/edit/(?P<agreement_detail_pk>\d+)/$',
        views.agreement_detail_edit, name="agreement_detail_edit"),
    url(r'^(?P<company_slug>[-\w]+)/detalis/(?P<agreement_pk>\d+)/delete/(?P<agreement_detail_pk>\d+)/$',
        views.agreement_detail_delete, name="agreement_detail_delete"),
]
