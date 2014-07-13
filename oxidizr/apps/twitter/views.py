# Imports from Django core
from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

# Imports from third party Django libs
from braces.views import LoginRequiredMixin, UserPassesTestMixin

# Imports from our custom apps
from apps.common.utils import not_logged_in_error_message, project_not_set_error_message

# Explicit imports from this app
from .models import Tweet, Account, APIKey
from .forms import CreateKeyForm


class TwitterIndexView(TemplateView):
    template_name = 'twitter/index.html'

    def get_context_data(self, **kwargs):
        context = super(TwitterIndexView, self).get_context_data(**kwargs)
        context['twitter_api_key'] = None
        if self.request.project.twitter_api_key:
            context['twitter_api_key'] = self.request.project.twitter_api_key.api_key
        return context


class CreateKeyView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'twitter/create_api_key.html'
    model = APIKey
    form_class = CreateKeyForm
    success_url = reverse_lazy('twitter_index')

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
        tokens = form.save(commit=False)
        tokens.project = self.request.project
        tokens.save()
        messages.add_message(
            message=_('Your Twitter application API keys have been saved!'),
            level=messages.SUCCESS,
            request=self.request,
            extra_tags='module-level'
        )
        return HttpResponseRedirect(reverse_lazy('twitter_index'))