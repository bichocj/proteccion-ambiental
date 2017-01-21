from django.conf.urls import url, patterns
from . import views

urlpatterns = patterns ("calendario.views",
	url(r'^', 'index', name='index'),

)