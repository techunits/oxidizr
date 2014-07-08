"""
Created on 06-Jul-2014

@author: brainless
"""
# Imports from system libraries
import datetime
import uuid

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
from .forms import LoginForm, RegistrationForm, EmailVerificationForm
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
        return reverse_lazy('job_list')

    def get_success_url(self):
        return reverse_lazy("job_list")

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
        return redirect(reverse_lazy('home_page'))


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
    template_name = 'auth/verification_start.html'
    form_class = EmailVerificationForm
    login_url = reverse_lazy('account_profile')
    user = None
    email_token = None

    def get_success_url(self):
        return reverse_lazy('home_page')

    def get_form_kwargs(self):
        kwargs = super(EmailVerificationView, self).get_form_kwargs()
        kwargs.update({
            'user_code': self.user.activation_code
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EmailVerificationView, self).get_context_data(**kwargs)
        user = self.user
        if self.request.GET.get('resend', None):
            user.send_verification_email()
        context['email'] = user.email
        return context

    def form_valid(self, form):
        user = self.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.is_email_verified = True
        user.is_active = True
        user.save()
        login(self.request, user)
        messages.add_message(
            message=_('Thank you for verifying your Email address, you are now logged in.'),
            request=self.request,
            level=messages.SUCCESS
        )
        return redirect(self.get_success_url())

    def test_func(self, user):
        if user.is_authenticated():
            if not user.is_email_validated:
                return True
            else:
                messages.add_message(
                    request=self.request,
                    level=messages.SUCCESS,
                    message=_('You have already verified your email address, please Login.')
                )
                self.login_url = reverse_lazy('login')
        else:
            if self.request.session.get('registration_user', None):
                try:
                    user = User.objects.get(id=self.request.session.get('registration_user', None))
                    if not user.is_email_validated:
                        self.user = user
                        return True
                    else:
                        messages.add_message(
                            request=self.request,
                            level=messages.SUCCESS,
                            message=_('You have already verified your email address, please Login.')
                        )
                        self.login_url = reverse_lazy('login')
                except User.DoesNotExist:
                    messages.add_message(
                        request=self.request,
                        level=messages.SUCCESS,
                        message=_('Sorry this email can not be verified, '
                                  'the user does not exist! Do you want to register?')
                    )
                    self.login_url = reverse_lazy('register')
        return False


class AccountVerificationView(TemplateView):
    template_name = "auth/verification_done.html"

    def get_context_data(self, **kwargs):
        context = super(AccountVerificationView, self).get_context_data(**kwargs)
        token = kwargs.get('token')
        try:
            user = User.objects.get(activation_code=token)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            if user and user.is_email_validated and user.is_active:
                context['state'] = "active"
            else:
                user.is_email_validated = True
                user.is_active = True
                user.save()
                context['state'] = "activated"
        except User.DoesNotExist:
            context['state'] = "invalid"
        return context


# class ForgotPasswordView(AnonymousRequiredMixin, CreateView):
#     form_class = ForgotRequestForm
#     template_name = 'auth/forgot_request.html'
#
#     def get_success_url(self):
#         return reverse_lazy('login')
#
#     def form_valid(self, form):
#         forgot_password = form.save(commit=False)
#
#         try:
#             user = User.objects.get(email=forgot_password.email)
#         except User.DoesNotExist:
#             form._errors['email'] = ErrorList([_('This email is not registered with us.')])
#             context = self.get_context_data(form=form)
#             return self.render_to_response(context)
#
#         forgot_password.token = uuid.uuid4().hex
#         forgot_password.save()
#         domain = get_current_site().domain
#         context = dict(
#             reset_link='http://%s%s' %
#                        (domain, reverse_lazy('reset-password', kwargs={'reset_code': forgot_password.token}))
#         )
#         email(
#             recipient=[forgot_password.email],
#             context=context,
#             template_name='reset_password',
#         )
#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             _('An Email has been sent to your email address with link to reset password.')
#         )
#         return redirect(self.get_success_url())
#
#
# class ResetPasswordView(AnonymousRequiredMixin, CreateView):
#     form_class = ResetPasswordForm
#     template_name = "account/reset_password.html"
#     model = PasswordResetToken
#
#     def get_success_url(self):
#         return reverse_lazy('login')
#
#     def form_valid(self, form):
#         cleaned_data = form.cleaned_data
#         context = self.get_context_data(form=form)
#         reset_code = self.kwargs['reset_code']
#
#         #check if passwords match
#         if cleaned_data['password'] != cleaned_data['repeat_password']:
#             form._errors['repeat_password'] = ErrorList([_("Given passwords do not match")])
#             return self.render_to_response(context)
#
#         forgot_password = self.forgot_password
#
#         #all hunky-dory; change the password, set the flag
#         user = User.objects.get(email=forgot_password.email)
#         user.set_password(cleaned_data['password'])
#         user.save()
#         forgot_password.retrieved = True
#         forgot_password.save()
#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             _('Password for your account has been changed successfully, you may login now.')
#         )
#         return redirect(self.get_success_url())
#
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             self.forgot_password = ForgotPassword.objects.get(
#                 token=self.kwargs.get('reset_code', None),
#                 retrieved=False)
#             return super(ResetPasswordView, self).dispatch(request, *args, **kwargs)
#         except ForgotPassword.DoesNotExist:
#             messages.add_message(
#                 request,
#                 messages.ERROR,
#                 _('Oops this password reset link has been used up.')
#             )
#             return redirect(reverse_lazy('login'))