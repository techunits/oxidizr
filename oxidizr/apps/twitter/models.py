import math

from django.db import models
from django.conf import settings


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
    We store all incoming tweets that match any keyword in our `keywords.BaseKeyword` model,
    regardless of who added the keyword. We filter our the tweets per project later in
     the `twitter.TweetPerProject` model.
    """
    author = models.ForeignKey('twitter.Account', blank=False, related_name='statuses')

    text = models.CharField(max_length=254, blank=False, null=False)
    tweet_id = models.CharField(max_length=100, unique=True)

    mentions = models.ManyToManyField('twitter.Account', related_name='mentioned_tweets')

    favorite_count = models.PositiveIntegerField(default=0)
    retweet_count = models.PositiveIntegerField(default=0)

    weight = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(blank=False, null=False)  # Passed in from Twitter, not our own

    projects = models.ManyToManyField('projects.Project', through='twitter.TweetPerProject')

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


class TweetPerProject(models.Model):
    """
    We sort of tweet for each project here. This is simply a mapping of tweets to project.
    This model is filled in asynchronously with background worked.
    """
    # TODO: write background job to fill this is
    tweet = models.ForeignKey('twitter.Tweet', blank=False, null=False)
    project = models.ForeignKey('projects.Project', blank=False, null=False)

    # Weight of a tweet will most probably vary for projects, depending on weight of keywords or other settings.
    weight = models.PositiveIntegerField(default=0)