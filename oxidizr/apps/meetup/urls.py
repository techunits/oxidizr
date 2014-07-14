from django.conf.urls import patterns, url

from .views import MeetupIndexView

urlpatterns = patterns(
    '',
    url(r'^$', MeetupIndexView.as_view(), name='meetup_index'),
)