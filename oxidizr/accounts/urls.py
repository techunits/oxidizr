from django.conf.urls import patterns, url

from .views import RegistrationView, LoginView, EmailVerificationView

urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name='accounts_login'),
    url(r'^register/$', RegistrationView.as_view(), name='accounts_register'),

    url(r'^email/(?P<id>\d+)/verify/$', EmailVerificationView.as_view(), name='accounts_email_verification'),
)