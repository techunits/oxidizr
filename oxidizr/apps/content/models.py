from django.db import models


class Content(models.Model):
    # site = models.ForeignKey('sites.Site', related_name='+')
    url = models.URLField(max_length=1000, blank=False, null=False, unique=True)
    title = models.CharField(max_length=1000, blank=False, null=False, db_index=True)
    summary = models.TextField(blank=True)

    added_at = models.DateTimeField(auto_now_add=True)
    # Updated from admin, or by client
    last_updated_at = models.DateTimeField(auto_now=True)
    last_crawled_at = models.DateTimeField()

    def __unicode__(self):
        return u'%s' % self.title
