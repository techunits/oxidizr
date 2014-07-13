from django.conf.urls import patterns, url

from .views import TwitterIndexView, CreateKeyView

urlpatterns = patterns(
    '',
    url(r'^$', TwitterIndexView.as_view(), name='twitter_index'),
    url(r'^api-keys/create/$', CreateKeyView.as_view(), name='twitter_create_api_key'),
)