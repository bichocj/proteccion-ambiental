from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin

from proteccion_ambiental import settings

urlpatterns = [
    url(r'^', include('main.urls', namespace="main")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^calendario/', include('fullcalendar.urls', namespace="fullcalendar")),
    url(r'^admin/', admin.site.urls),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
