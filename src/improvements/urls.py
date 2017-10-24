from django.conf.urls import url

from improvements import views

urlpatterns = [
    # url(r'^(?P<company_slug>[-\w]+)/$', views.home, name="home"),
    # Metting
    url(r'^(?P<company_slug>[-\w]+)/list/$', views.meeting_list, name="meeting_list"),
    url(r'^(?P<company_slug>[-\w]+)/new/$', views.meeting_new, name="meeting_new"),
    url(r'^(?P<company_slug>[-\w]+)/edit/(?P<meeting_pk>[-\w]+)/',
        views.meeting_edit, name="meeting_edit"),
    url(r'^(?P<company_slug>[-\w]+)/delete/(?P<meeting_pk>[-\w]+)/',
        views.meeting_delete, name="meeting_delete"),
    # Agreements
    url(r'^(?P<company_slug>[-\w]+)/(?P<meeting_pk>[-\w]+)/agreements/list/$', views.agreement_list,
        name="agreement_list"),
    url(r'^(?P<company_slug>[-\w]+)/(?P<meeting_pk>[-\w]+)/agreements/new/$', views.agreement_new,
        name="agreement_new"),
    url(r'^(?P<company_slug>[-\w]+)/(?P<meeting_pk>[-\w]+)/agreements/desactivar/(?P<agreement_pk>\d+)/$',
        views.desactive_agreement,
        name="desactive_agreement"),
    url(r'^(?P<company_slug>[-\w]+)/(?P<meeting_pk>[-\w]+)/agreements/edit/(?P<agreement_pk>\d+)/$',
        views.agreement_edit, name="agreement_edit"),
    url(r'^(?P<company_slug>[-\w]+)/(?P<meeting_pk>[-\w]+)/agreements/delete/(?P<agreement_pk>\d+)/$',
        views.agreement_delete, name="agreement_delete"),
    # Agremment Details
    url(r'^(?P<company_slug>[-\w]+)/detalis/(?P<agreement_pk>\d+)/$', views.agreement_detail, name="agreement_detail"),

    url(r'^(?P<company_slug>[-\w]+)/detalis/(?P<agreement_pk>\d+)/new/$', views.agreement_detail_new, name="agreement_detail_new"),

    url(r'^(?P<company_slug>[-\w]+)/detalis/(?P<agreement_pk>\d+)/edit/(?P<agreement_detail_pk>\d+)/$',
        views.agreement_detail_edit, name="agreement_detail_edit"),
    url(r'^(?P<company_slug>[-\w]+)/detalis/(?P<agreement_pk>\d+)/delete/(?P<agreement_detail_pk>\d+)/$',
        views.agreement_detail_delete, name="agreement_detail_delete"),
]
