from fullcalendar import views

__author__ = 'jona'

from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<company_slug>[-\w]+)/list/$', views.calendar_list, name="calendar_list"),
    url(r'^(?P<company_slug>[-\w]+)/new/$', views.calendar_new, name="new"),
    url(r'^(?P<company_slug>[-\w]+)/edit/(?P<calendar_id>\d+)/$', views.calendar_edit, name="edit"),
    url(r'^(?P<company_slug>[-\w]+)/delete/(?P<calendar_id>\d+)/$', views.calendar_delete, name="delete"),

    url(r'^(?P<company_slug>[-\w]+)/view/(?P<slug>[-\w]+)/(?P<calendar_id>\d+)/$', views.view_calendar,
        name="view_calendar"),
    url(r'^events/(?P<calendar_id>\d+)/$', views.events_json, name="events_json"),
    url(r'^event/save/(?P<slug>[-\w]+)$', views.save_event, name="save_event"),
    url(r'^event/$', views.get_event, name="get_event"),
    url(r'^event/update/', views.update_event, name="update_event"),
    url(r'^settings/(?P<slug>[-\w]+)/$', views.settings_calendar, name="settings_calendar")
]
