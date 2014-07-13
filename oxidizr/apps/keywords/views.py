# Imports from Django core
from django.views.generic import View, TemplateView, ListView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect
from django.db.utils import IntegrityError

# Imports from third party Django libs
from braces.views import LoginRequiredMixin, JSONResponseMixin, UserPassesTestMixin

# Imports from our custom apps
from apps.common.utils import not_logged_in_error_message, project_not_set_error_message

# Explicit imports from this app
from .models import BaseKeyword, Keyword
from .forms import KeywordCreateForm


class KeywordIndexView(TemplateView):
    template_name = 'keywords/index.html'


class KeywordManageView(LoginRequiredMixin, ListView):
    model = Keyword
    template_name = 'keywords/manage.html'
    context_object_name = 'keywords'

    def get_queryset(self):
        if self.request.project:
            return Keyword.objects.filter(project=self.request.project)
        else:
            return None


class KeywordCreateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    model = Keyword
    form_class = KeywordCreateForm
    template_name = 'keywords/create.html'
    success_url = reverse_lazy('keywords_manage')

    def test_func(self, user):
        if self.request.project:
            return True
        return False

    def get_login_url(self):
        if not self.request.user.is_authenticated():
            not_logged_in_error_message(self.request)
            return reverse_lazy('accounts_login')
        if not self.request.project:
            project_not_set_error_message(self.request)
            return reverse_lazy('projects_index')

    def form_valid(self, form):
        base, created = BaseKeyword.objects.get_or_create(term=form.cleaned_data['term'])
        keyword = Keyword()
        keyword.base = base
        keyword.project = self.request.project
        try:
            keyword.save()
        except IntegrityError:
            # The unique_together constraint on Keyword model failed
            # TODO: Handle a more specific error, IntegrityError could be raised by things other than duplicate too
            messages.add_message(
                message=_('You already have that keyword for this project, so we did not add it again.'),
                level=messages.INFO,
                request=self.request,
                extra_tags='module-level'
            )
        return HttpResponseRedirect(self.get_success_url())


class KeywordDeleteView(LoginRequiredMixin, JSONResponseMixin, View):
    pass