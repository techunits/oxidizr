from django.views.generic import TemplateView


class WebsiteIndexView(TemplateView):
    template_name = 'websites/index.html'