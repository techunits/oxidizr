from django.conf.urls import patterns, url

from .views import RegistrationView, LoginView, LogoutView, EmailVerificationView, ForgotPasswordView

urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name='accounts_login'),
    url(r'^register/$', RegistrationView.as_view(), name='accounts_register'),
    url(r'^logout/$', LogoutView.as_view(), name='accounts_logout'),

    url(r'^password/forgot/$', ForgotPasswordView.as_view(), name='accounts_forgot_password'),

    url(r'^email/(?P<id>\d+)/verify/$', EmailVerificationView.as_view(), name='accounts_email_verification'),
)