# Imports from system libraries
import re
import random

# Imports from Django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.core import validators

# Imports from custom apps
from apps.common.utils import email


class User(AbstractBaseUser):
    username = models.CharField(
        _('Username'),
        max_length=30,
        blank=False,
        null=False,
        unique=True,
        help_text=_('30 characters or fewer. Letters, numbers and ./-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.\-_]+$'), _('Enter a valid username.'), 'invalid')
        ]
    )
    first_name = models.CharField(_('First Name'), max_length=30, blank=False, null=False)
    middle_name = models.CharField(_('Middle Name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=30, blank=False, null=False)
    email = models.EmailField(
        _('Email Address'),
        blank=False,
        null=False,
        db_index=True,
        unique=True,
        help_text=_("Required, please use your personal Email Address"))
    date_of_birth = models.DateField(blank=True, null=True)

    # Status checks
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('Is active?'),
        default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_superuser = models.BooleanField(default=False, blank=False, null=False)
    is_email_verified = models.BooleanField(default=False, blank=False, null=False)

    # Dates and Times
    verification_code = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_from_ip = models.CharField(max_length=50, null=True, blank=True)
    last_activity_checked_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse_lazy("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name.capitalize(), self.last_name.capitalize())
        return full_name.strip()

    def get_short_name(self):
        if self.first_name and self.last_name:
            return '%s %s.' % (self.first_name.capitalize(), self.last_name[0])
        else:
            return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def send_verification_email(self, rehash=False):
        if not self.activation_code or rehash:
            self.activation_code = random.randint(111111, 999999)
            self.save()
        context = dict(
            activation_code=self.activation_code,
            first_name=self.first_name
        )
        email(
            recipient=[self.email],
            context=context,
            template_name='activate_email'
        )

    def __unicode__(self):
        return u'%s' % self.username

    def __str__(self):
        return '%s' % self.username