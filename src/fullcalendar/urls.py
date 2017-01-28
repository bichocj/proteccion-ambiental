__author__ = 'jona'

from django.conf.urls import url, patterns

urlpatterns = patterns('fullcalendar.views',
                       url(r'^list/$', "calendar_list", name="calendar_list"),
                       url(r'^new/$', "new_calendar", name="new_calendar"),
                       url(r'^view/(?P<slug>[-\w]+)/(?P<calendar_id>\d+)/$', "view_calendar", name="view_calendar"),
                       url(r'^events/(?P<calendar_id>\d+)/$', "events_json", name="events_json"),
                       url(r'^event/save/(?P<slug>[-\w]+)$', "save_event", name="save_event"),
                       url(r'^event/$', "get_event", name="get_event"),
                       url(r'^event/update/', "update_event", name="update_event"),
                       url(r'^settings/(?P<slug>[-\w]+)/$', "settings_calendar", name="settings_calendar")
                       )
