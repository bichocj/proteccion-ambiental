from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^', include('main.urls', namespace="main")),
	url(r'^accounts/', include('accounts.urls', namespace="accounts")),
	url(r'^calendario/', include('calendario.urls', namespace="calendario")),
	url(r'^admin/', admin.site.urls),
]