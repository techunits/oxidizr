from django.db import models


class Keyword(models.Model):
    term = models.CharField(max_length=50, blank=False, null=False)


class Event(models.Model):
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

    def __unicode__(self):
        return self.name