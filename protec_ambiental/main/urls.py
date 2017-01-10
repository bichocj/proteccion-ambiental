from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

urlpatterns = patterns('main.views',
               url(r'^$', 'home', name='home'),
               url(r'^oshas/$', 'oshas', name='oshas'),   
               url(r'^law/$', 'law', name='law'),   

           )
