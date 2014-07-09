"""
Created on 06-Jul-2014

@author: brainless
"""
# Imports from system libraries
import datetime
import uuid
import pytz

# Imports from Django
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, FormView, View, CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.forms.util import ErrorList
from django.contrib import messages

# Imports from third party Django apps/libraries
from braces.views import UserPassesTestMixin, AnonymousRequiredMixin

# Imports from custom apps/libraries
from apps.common.utils import email, get_current_site, get_client_ip

# Explicit imports from this app
from .forms import LoginForm, RegistrationForm, EmailVerificationForm, ForgotPasswordForm, ResetPasswordForm
from .models import EmailVerificationCode, PasswordResetCode


User = get_user_model()


class LoginView(AnonymousRequiredMixin, FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_authenticated_redirect_url(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _('You are already logged in')
        )
        return reverse_lazy('home_page')

    def get_success_url(self):
        return reverse_lazy('home_page')

    def form_valid(self, form):
        user_email = form.cleaned_data['email'].lower().strip()
        password = form.cleaned_data['password']
        user = authenticate(email=user_email, password=password)
        if user and user.is_active:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            try:
                user = User.objects.get(email__iexact=user_email)
                if not check_password(password, user.password):
                    form._errors['password'] = ErrorList([u'That is not the correct Password.'])
            except User.DoesNotExist:
                form._errors['email'] = ErrorList([u'This email is not registered with us.'])
            context = self.get_context_data(form=form)
            return self.render_to_response(context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('welcome_page'))


class RegistrationView(AnonymousRequiredMixin, FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm
    email_token = None

    def get_success_url(self):
        return reverse_lazy('accounts_email_verification', kwargs={'id': self.email_token.id})

    def form_valid(self, form, *args, **kwargs):
        cleaned_data = form.cleaned_data
        cleaned_data.pop('repeat_password')
        password = cleaned_data.pop('password')
        user = User.objects.create(**cleaned_data)
        user.set_password(password)
        user.date_joined = datetime.datetime.now()
        user.created_from_ip = get_client_ip(self.request)
        user.save()

        # Generate an email verification token for this user's email address
        email_token = EmailVerificationCode()
        email_token.email = user.email
        email_token.owner = user
        email_token.save()
        email_token.send_email()
        self.email_token = email_token

        messages.add_message(
            request=self.request,
            level=messages.SUCCESS,
            message=_('Thank you for signing up!')
        )
        self.request.session['registration_process'] = True
        # We are not going to login the user, but allow them to use certain forms
        self.request.session['registration_user'] = user.id
        return redirect(self.get_success_url())


class EmailVerificationView(UserPassesTestMixin, FormView):
    template_name = 'accounts/email_verification.html'
    form_class = EmailVerificationForm
    user = None
    email_token = None

    def get_success_url(self):
        return reverse_lazy('home_page')

    def get_form_kwargs(self):
        kwargs = super(EmailVerificationView, self).get_form_kwargs()
        kwargs.update({
            'email_token': self.email_token
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EmailVerificationView, self).get_context_data(**kwargs)
        user = self.user
        context['email_token'] = self.email_token
        context['email'] = user.email
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('resend', None):
            self.email_token.send_email()
            return redirect(reverse_lazy('accounts_email_verification', args=(self.email_token.id,)))
        return super(EmailVerificationView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.is_email_verified = True
        user.is_active = True
        user.save()

        email_token = self.email_token
        email_token.verified_from_ip = get_client_ip(self.request)
        email_token.verified_at = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        email_token.save()

        login(self.request, user)
        messages.add_message(
            message=_('Thank you for verifying your Email address, you are now logged in.'),
            request=self.request,
            level=messages.SUCCESS
        )
        return redirect(self.get_success_url())

    def test_func(self, user):
        if not user.is_authenticated() and self.request.session.get('registration_user', None):
            try:
                user = User.objects.get(id=self.request.session.get('registration_user', None))
                if not user.is_email_verified:
                    self.email_token = EmailVerificationCode.objects.get(
                        id=self.kwargs.get('id'),
                        email=user.email,
                        verified_at=None,
                        owner=user
                    )
                    self.user = user
                    return True
                else:
                    messages.add_message(
                        request=self.request,
                        level=messages.SUCCESS,
                        message=_('You have already verified your email address, please Login.')
                    )
            except User.DoesNotExist:
                messages.add_message(
                    request=self.request,
                    level=messages.SUCCESS,
                    message=_('Sorry this email can not be verified, '
                              'the user does not exist! Do you want to register?')
                )
        return False

    def get_login_url(self):
        if self.request.user.is_authenticated():
            return reverse_lazy('home_page')
        else:
            return reverse_lazy('accounts_register')


class ForgotPasswordView(AnonymousRequiredMixin, FormView):
    form_class = ForgotPasswordForm
    template_name = 'accounts/forgot_password.html'
    password_token = None

    def get_success_url(self):
        return reverse_lazy('accounts_reset_password', args=(self.password_token.id,))

    def form_valid(self, form):
        email_address = form.cleaned_data['email']

        try:
            user = User.objects.get(email=email_address)
        except User.DoesNotExist:
            form._errors['email'] = ErrorList([_('This email is not registered with us.')])
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

        password_token = PasswordResetCode()
        password_token.owner = user
        password_token.save()
        password_token.send_email()
        self.password_token = password_token

        messages.add_message(
            request=self.request,
            level=messages.SUCCESS,
            message=_('An Email has been sent to your email address (%s) with '
                      'verification code to reset the password.' % email_address),
            extra_tags='page-level'
        )
        return redirect(self.get_success_url())


class ResetPasswordView(AnonymousRequiredMixin, FormView):
    form_class = ResetPasswordForm
    template_name = 'accounts/reset_password.html'
    model = PasswordResetCode

    def get_success_url(self):
        return reverse_lazy('accounts_login')

    def form_valid(self, form):
        form_data = form.cleaned_data

        try:
            one_hour_ago = datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(hours=1)
            password_token = PasswordResetCode.objects.get(
                verification_code=form_data['verification_code'],
                created_at__gt=one_hour_ago
            )
            owner = password_token.owner
            owner.set_password(form_data['password'])
            owner.save()
            messages.add_message(
                message=_('Your password has been successfully reset, you may login now.'),
                level=messages.SUCCESS,
                request=self.request,
                extra_tags='page-level'
            )
            return redirect(self.get_success_url())
        except PasswordResetCode.DoesNotExist:
            form._errors['verification_code'] =\
                ErrorList([_('The verification code does not match the one we sent you in Email.')])
            context = self.get_context_data(form=form)
            return self.render_to_response(context)