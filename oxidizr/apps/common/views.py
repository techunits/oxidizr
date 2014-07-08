from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('welcome_page')
    template_name = 'common/home.html'