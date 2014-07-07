from django.conf.urls import patterns, url

from .views import RegistrationView, LoginView

urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name='accounts_login'),
    url(r'^register/$', RegistrationView.as_view(), name='accounts_register'),
)