import sendgrid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from sendgrid.helpers.mail import *

from accounts.forms import PasswordResetFormEdited
from accounts.functions import get_member_group
from main.models import Company
from proteccion_ambiental.settings import DEFAULT_EMAIL, SENDGRID_KEY, FROM_NAME
from main.functions import send_email


def message(request, code):
    if code == 'password_reset':
        message = _(
            '<strong>We have sent you an email!</strong> Please, follow the instructions to reset your password.')
        # messages.add_message(request, messages.INFO, message)
        return render(request, 'accounts/echo.html', locals())
        # return redirect(reverse('accounts:password_reset'))

    if code == 'password_reset_confirm':
        messages.add_message(request, messages.INFO, _(
            '<strong>Success!</strong> You have changed your password.'))
        return redirect(reverse('accounts:login'))

    if code == 'password_change_done':
        messages.add_message(request, messages.INFO, _(
            '<strong>Success!</strong> You have changed your password.'))
        return redirect(reverse('accounts:password_change'))

    return redirect(reverse('accounts:profile_edit'))


@csrf_protect
def password_reset(request):
    title = _('Reset password')
    from_email = 'no-reply@oneventus.com'
    domain = get_current_site(request)
    site_name = get_current_site(request)
    contact_email = DEFAULT_EMAIL
    # TODO put like setting value

    if request.method == "POST":
        form = PasswordResetFormEdited(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            for user in form.get_users(email):
                context = {
                    'email': user.email,
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                    'main_email': contact_email,
                }

                text_content = get_template('accounts/email/email_reset.html').render(context)
                html_content = get_template('accounts/email/email_reset.html').render(context)

                subject = loader.render_to_string('registration/password_reset_subject.txt', context)
                subject = ''.join(subject.splitlines())

                send_email(FROM_NAME, DEFAULT_EMAIL, email, subject, text_content, html_content)

            return HttpResponseRedirect('/accounts/message/password_reset/')
    else:
        form = PasswordResetFormEdited()

    return render(request, 'accounts/password_reset.html', locals())


@login_required
def admin_workes(request, company_slug):
    company = Company.objects.get(pk=company_slug)
    return


@csrf_exempt
@login_required
def get_members(request):
    pattern = request.GET.get('pattern')

    if pattern:
        objects = get_member_group().user_set.values('pk', 'first_name', 'last_name').filter(
            Q(first_name__icontains=pattern) | Q(last_name__icontains=pattern))
    else:
        objects = []
    s_json = json.dumps(list(objects))
    return HttpResponse(s_json, content_type='application/json')
