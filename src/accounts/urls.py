from django.conf.urls import  url
from django.utils.translation import ugettext as _
from . import views
from django.contrib.auth import views as vi

from accounts.forms import SetPasswordFormEdited, AuthenticationFormEdited

urlpatterns = [
                       url(r'^message/(?P<code>[-\w]+)/$', views.message, name='message'),
                       url(r'^profile/password/reset/$', views.password_reset, name='password_reset'),
                       url(r'^get-members/$', views.get_members, name='get_members'),
                       url(r'^workers/(?P<company_slug>[-\w]+)/$', views.admin_workes, name='admin_workes'),
]
urlpatterns += [
                        url(r'^login/$', vi.login, {
                            'template_name': 'accounts/login.html',
                            'authentication_form': AuthenticationFormEdited,
                            'extra_context': {
                                'page': {
                                    'title': _('Log in'),
                                },
                            }
                        }, name='login'),
                        url(r'^logout/$', vi.logout, {
                            'next_page': '/',
                        }, name='logout'),
                        url(r'^profile/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                            vi.password_reset_confirm, {
                                'template_name': 'accounts/password_reset_confirm.html',
                                'set_password_form': SetPasswordFormEdited,
                                'post_reset_redirect': '/accounts/message/password_reset_confirm/',
                            }, 'password_reset_confirm', ),

                        ]

