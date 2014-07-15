import math

from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_weight(follower_count=1, following_count=1, status_count=1, listed_in_count=1, is_verified=False):
    """
    (Follower_count / Following_count) + status_count + listed_in_count
    """
    if not follower_count and not following_count and not status_count:
        return 0
    if not follower_count:
        follower_count = 1
    if not following_count:
        following_count = 1
    if not status_count:
        status_count = 1
    if not listed_in_count:
        listed_in_count = 1
    return int((follower_count / following_count) *
               math.log10(follower_count) +
               2 * listed_in_count) + 50 * bool(is_verified)


class Tweet(models.Model):
    """
    We store all incoming tweets that match any keyword in our `keywords.Keyword` model,
    regardless of who added the keyword, as long as it is enabled for Twitter.
    We filter out the tweets per project in the `twitter.TweetPerProject` model.
    """
    author = models.ForeignKey('twitter.Account', blank=False, related_name='statuses')

    text = models.CharField(max_length=254, blank=False, null=False)
    tweet_id = models.CharField(max_length=100, unique=True)

    mentions = models.ManyToManyField('twitter.Account', related_name='mentioned_tweets')

    favorite_count = models.PositiveIntegerField(default=0)
    retweet_count = models.PositiveIntegerField(default=0)

    weight = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(blank=False, null=False)  # Passed in from Twitter, not our own

    projects = models.ManyToManyField('projects.Project', through='twitter.TweetPerProject', related_name='tweets')

    def view_tweet(self):
        return '<a href="https://twitter.com/%s/statuses/%s" target="_blank">View</a>' %\
               (self.author.screen_name, self.tweet_id)
    view_tweet.short_description = 'View Tweet'
    view_tweet.allow_tags = True

    def __unicode__(self):
        return u'%s' % self.text

    @property
    def tweet_link(self):
        return 'https://twitter.com/%s/statuses/%s' %\
               (self.author.screen_name, self.tweet_id)


class Account(models.Model):
    twitter_id = models.CharField(max_length=100, unique=True)
    screen_name = models.CharField(max_length=60, blank=False, null=False)
    name = models.CharField(max_length=140, blank=False, null=False)

    url = models.CharField(max_length=254, blank=True, null=True)

    status_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    listed_in_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    weight = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.weight:
            self.weight = get_weight(self.follower_count, self.following_count,
                                     self.status_count, self.listed_in_count, self.is_verified)
        super(Account, self).save(*args, **kwargs)

    def get_weight(self):
        return get_weight(self.follower_count, self.following_count,
                          self.status_count, self.listed_in_count, self.is_verified)
    get_weight.short_description = 'Weight'


class APIKey(models.Model):
    """
    This model stores the Twitter OAuth access token, secret etc. for each project.
    To create on for any project, simply head over to https://apps.twitter.com/
    Create a new app and then generate access token. Frontend Oxidizr app has clear instructions.
    """
    project = models.OneToOneField('projects.Project', blank=False, null=False, related_name='twitter_api_key')

    api_key = models.CharField(_('API key'), max_length=250, blank=False, null=False)
    api_secret = models.CharField(_('API secret'), max_length=250, blank=False, null=False)
    consumer_key = models.CharField(_('Access token'), max_length=250, blank=False, null=False)
    consumer_secret = models.CharField(_('Access token secret'), max_length=250, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)


class TweetPerProject(models.Model):
    """
    This model is the through table for relation between `twitter.Tweet` and `keywords.Keyword`.
    """
    # TODO: write background job to fill this is
    tweet = models.ForeignKey('twitter.Tweet', blank=False, null=False)
    project = models.ForeignKey('projects.Project', blank=False, null=False)

    # Weight of a tweet will vary for each project, depending on weight of keywords or other factors.
    weight = models.PositiveIntegerField(default=0)