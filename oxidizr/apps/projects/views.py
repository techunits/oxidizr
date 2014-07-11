from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from braces.views import LoginRequiredMixin

from .models import Project


class ProjectIndexView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('id', None):
            try:
                Project.objects.get(id=self.kwargs.get('id', None), owner=request.user)
                request.session['default_project_id'] = self.kwargs.get('id', None)
            except Project.DoesNotExist:
                messages.add_message(
                    message=_('Sorry we could not find that project'),
                    level=messages.ERROR,
                    request=request,
                    extra_tags='danger page-level'
                )
            return redirect(reverse_lazy('projects_index'))
        return super(ProjectIndexView, self).get(request, *args, **kwargs)


class ProjectManageView(LoginRequiredMixin, ListView):
    pass