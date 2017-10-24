from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from proteccion_ambiental import settings

urlpatterns = [
                  url(r'^accounts/', include('accounts.urls', namespace="accounts")),
                  url(r'^calendario/', include('fullcalendar.urls', namespace="fullcalendar")),
                  url(r'^acuerdos/', include('acuerdos_sst.urls', namespace="acuerdos_sst")),
                  url(r'^mejoras/', include('improvements.urls', namespace="improvements")),
                  url(r'^admin/', admin.site.urls),
                  url(r'^', include('main.urls', namespace="main")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
