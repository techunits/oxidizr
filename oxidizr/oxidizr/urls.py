from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from apps.common.views import HomePageView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomePageView.as_view(), name='home_page'),
    url(r'^$', HomePageView.as_view(), name='home_page'),

    url(r'^welcome/$', TemplateView.as_view(template_name='welcome.html'), name='welcome_page'),

    url(r'^accounts/', include('accounts.urls')),

    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
)