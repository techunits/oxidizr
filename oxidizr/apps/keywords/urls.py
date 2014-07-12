# Imports from Django core
from django.conf.urls import patterns, url

# Explicit imports from this app
from .views import (
    KeywordManageView, KeywordCreateView, KeywordDeleteView,
    KeywordIndexView
)


urlpatterns = patterns(
    '',
    url(r'^$', KeywordIndexView.as_view(), name='keywords_index'),
    url(r'^manage/$', KeywordManageView.as_view(), name='keywords_manage'),
    url(r'^create/$', KeywordCreateView.as_view(), name='keywords_create'),
    url(r'^(?P<slug>[\w-]+)/delete/$', KeywordDeleteView.as_view(), name='keywords_delete')
)