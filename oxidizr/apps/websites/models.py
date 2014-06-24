from django.db import models


class Website(models.Model):
    url = models.URLField(max_length=155, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)

    # We DO NOT want to crawl this site
    is_banned = models.BooleanField(default=False)

    # Crawler will do depth first
    is_deep_crawl = models.BooleanField(default=False)

    # By client, from admin, or by crawler
    added_at = models.DateTimeField(auto_now_add=True)
    # Updated from admin, or by client
    last_updated_at = models.DateTimeField(auto_now=True)
    last_crawled_at = models.DateTimeField()

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name.encode('ascii', 'ignore')