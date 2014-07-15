from django.db import models


class Event(models.Model):
    """
    We store all discovered events from Meetup.com in this model.
    Events matching any keywords in `keywords.Keyword` model, in the name or description are stored here,
     regardless of who added the keyword, as long as the keyword is enabled for Meetup.com
    """
    event_id = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=300, blank=False, null=False)
    event_url = models.URLField(blank=False, null=False)
    description = models.TextField(blank=True)
    group_url = models.URLField(blank=False, null=False)
    photo_url = models.URLField(blank=True)

    when = models.DateTimeField(blank=False)
    venue_city = models.CharField(max_length=60, blank=True)
    venue_country = models.CharField(max_length=60, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    projects = models.ManyToManyField('projects.Project', through='meetup.EventPerProject', related_name='meetup_events')

    def __unicode__(self):
        return self.name


class EventPerProject(models.Model):
    """
    This model is the through table for relation between `meetup.Event` and `keywords.Keyword`
    """
    event = models.ForeignKey('meetup.Event', blank=False, null=False)
    project = models.ForeignKey('projects.Project', blank=False, null=False)

    # Weight of an event will vary for each project, depending on weight of keywords or other factors.
    weight = models.PositiveIntegerField(default=0)