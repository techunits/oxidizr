from django.views.generic import TemplateView


class MeetupIndexView(TemplateView):
    template_name = 'meetup/index.html'