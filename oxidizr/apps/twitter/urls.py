from django.conf.urls import patterns, url

from .views import TwitterIndexView

urlpatterns = patterns(
    '',
    url(r'^$', TwitterIndexView.as_view(), name='twitter_index'),
)