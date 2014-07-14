from django.views.generic import TemplateView


class ContentIndexView(TemplateView):
    template_name = 'content/index.html'