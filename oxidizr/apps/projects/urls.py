from django.conf.urls import patterns, url

from .views import (
    ProjectIndexView, ProjectManageView
)

urlpatterns = patterns(
    '',
    url(r'^$', ProjectIndexView.as_view(), name='projects_index'),
    url(r'^default/(?P<id>\d+)/$', ProjectIndexView.as_view(), name='projects_set_default'),

    url(r'^manage/$', ProjectManageView.as_view(), name='projects_manage')
)