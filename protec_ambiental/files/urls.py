from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

urlpatterns = patterns('files.views',
               url(r'^$', 'Entrada', name='Entrada'),
           )
