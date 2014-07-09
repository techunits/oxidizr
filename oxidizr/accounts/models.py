# Imports from system libraries
import re

# Imports from Django
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.core import validators

# Imports from custom apps
from apps.common.utils import email, generate_random_string, get_current_site


class User(AbstractBaseUser):
    username = models.CharField(
        _('Username'),
        max_length=30,
        blank=False,
        null=False,
        unique=True,
        help_text=_('30 characters or fewer. Letters, numbers and ./-/_ characters'),
        validators=[
            validators.RegexValidator('^[\w.\-_]+$', _('Enter a valid username.'), 'invalid')
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
    date_joined = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    notifications_checked_at = models.DateTimeField(null=True, blank=True)

    # IP address log
    created_from_ip = models.GenericIPAddressField(null=True, blank=True)

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

    def __unicode__(self):
        return u'%s' % self.username

    def __str__(self):
        return '%s' % self.username


class EmailVerificationCode(models.Model):
    """
    This model holds email verification tokens for verifying email addresses.
    We store the email address since we want to have the possibility of multiple email addresses.
    """
    email = models.EmailField(unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='+')
    verification_code = models.CharField(max_length=50, null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    verified_at = models.DateTimeField(blank=True, null=True)

    verified_from_ip = models.GenericIPAddressField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.email

    def __str__(self):
        return '%s' % self.email

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = generate_random_string(8).upper()
        super(EmailVerificationCode, self).save(*args, **kwargs)

    def generate_token(self):
        self.verification_code = generate_random_string(8).upper()
        self.save()

    def send_email(self, regenerate=False):
        if not self.verification_code or regenerate:
            self.generate_token()
        context = dict(
            verification_code=self.verification_code,
            first_name=self.owner.first_name
        )
        email(
            recipient=[self.email],
            context=context,
            template_name='email_verification'
        )


class PasswordResetCode(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)
    verification_code = models.CharField(max_length=50, null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    reset_at = models.DateTimeField(blank=True, null=True)

    reset_from_ip = models.GenericIPAddressField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.owner

    def __str__(self):
        return '%s' % self.owner

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = generate_random_string(24).upper()
        super(PasswordResetCode, self).save(*args, **kwargs)

    def generate_token(self):
        self.verification_code = generate_random_string(24).upper()
        self.save()

    def send_email(self, regenerate=False):
        if not self.verification_code or regenerate:
            self.generate_token()

        context = dict(
            verification_code=self.verification_code,
            first_name=self.owner.first_name,
            accounts_reset_password_link='http://%s%s' % (
                get_current_site().domain,
                reverse_lazy('accounts_reset_password', args=(self.id,))
            )
        )
        email(
            recipient=[self.owner.email],
            context=context,
            template_name='password_reset'
        )