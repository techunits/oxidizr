# Imports from Django core
from django.conf.urls import patterns, url

# Explicit imports from this app
from .views import KeywordManageView, KeywordCreateView, KeywordUpdateView, KeywordDeleteView


urlpatterns = patterns(
    '',
    url(r'^manage/$', KeywordManageView.as_view(), name='keywords_manage'),
    url(r'^create/$', KeywordCreateView.as_view(), name='keywords_create'),
    url(r'^(?P<slug>[\w-]+)/update/$', KeywordUpdateView.as_view(), name='keywords_update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', KeywordDeleteView.as_view(), name='keywords_delete')
)