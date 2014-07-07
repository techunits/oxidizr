import random
import string

import django
from django.conf import settings
from django.contrib.sites.models import Site

from post_office import mail, PRIORITY
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def generate_random_string(length, stringset=None):
    '''
    Returns a string with `length` characters chosen from `stringset`
    >>> len(generate_random_string(20)) == 20
    '''
    if not stringset:
        stringset = string.ascii_uppercase.replace('I', '').replace('O', '') +\
                    string.digits.replace('0', '').replace('1', '')
    return ''.join([random.choice(stringset) for n in range(length)])


def get_current_site():
    return Site.objects.get_current()


def email(recipient, context, template_name, sender=None):
    if not settings.MANDRILL_API_KEY or settings.MANDRILL_API_KEY == 'None':
        return
    current_site = Site.objects.get_current()
    context['domain'] = current_site.domain
    User = django.contrib.auth.get_user_model()
    # The recipient list can be a list of User model instances or Email Address string
    # Which means you could pass a User model QuerySet as recipient
    # If a recipient is User model instance then simple convert to Email Address string
    recipient_email_list = []
    for rec in recipient:
        if isinstance(rec, User):
            if rec.first_name and rec.last_name:
                recipient_email_list.append('"%s %s" <%s>' % (rec.first_name, rec.last_name, rec.email))
            elif rec.first_name:
                recipient_email_list.append('"%s" <%s>' % (rec.first_name, rec.email))
            else:
                recipient_email_list.append('%s' % rec.email)
        else:
            recipient_email_list.append(rec)

    mail.send(
        sender=sender or settings.DEFAULT_FROM_EMAIL,
        recipients=recipient_email_list,
        template=template_name,
        context=context,
        priority=PRIORITY.now
    )


def custom_template_constants(request):
    return dict(
        DATE_FORMAT_PYTHON=settings.DATE_FORMAT_PYTHON,
        DATE_FORMAT_JS=settings.DATE_FORMAT_JS,
        DATE_FORMAT_TEMPLATE=settings.DATE_FORMAT_TEMPLATE,

        TIME_FORMAT_PYTHON=settings.TIME_FORMAT_PYTHON,
        TIME_FORMAT_JS=settings.TIME_FORMAT_JS,
        TIME_FORMAT_TEMPLATE=settings.TIME_FORMAT_TEMPLATE,

        DATETIME_FORMAT_TEMPLATE=settings.DATETIME_FORMAT_TEMPLATE
    )


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip