# Imports from Django core
from django.views.generic import View

# Imports from third party Django libs
from braces.views import LoginRequiredMixin, JSONResponseMixin

# Imports from our custom apps

# Explicit imports from this app
from .models import BaseKeyword, Keyword


class KeywordManageView(LoginRequiredMixin, JSONResponseMixin, View):
    pass


class KeywordCreateView(LoginRequiredMixin, JSONResponseMixin, View):
    pass


class KeywordUpdateView(LoginRequiredMixin, JSONResponseMixin, View):
    pass


class KeywordDeleteView(LoginRequiredMixin, JSONResponseMixin, View):
    pass