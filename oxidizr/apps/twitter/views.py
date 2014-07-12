from django.views.generic import TemplateView


class TwitterIndexView(TemplateView):
    template_name = 'twitter/index.html'