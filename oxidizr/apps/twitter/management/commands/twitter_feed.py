from twitter import OAuth, TwitterStream
from dateutil import parser

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.utils import IntegrityError

from apps.twitter.models import Keyword, Tweet, Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Keyword.objects.count():
            raise CommandError("Please specify some keywords in the admin for Twitter feed to work")
        keywords = ','.join([k['term'] for k in Keyword.objects.values('term')])
        twitter_stream = TwitterStream(auth=OAuth(
            token=settings.TWITTER_TOKEN,
            token_secret=settings.TWITTER_TOKEN_SECRET,
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET))
        stream = twitter_stream.statuses.filter(track=keywords)

        for tweet in stream:
            if 'retweeted_status' in tweet:
                # If this is a retweet of an earlier tweet, then we want to check only the original.
                tweet = tweet['retweeted_status']
            user = tweet['user']

            author = Account(
                twitter_id=user['id_str'],
                screen_name=user['screen_name'],
                name=user['name'],
                url=user['url'] if 'url' in user else None,
                status_count=user['statuses_count'] if 'statuses_count' in user else 0,
                follower_count=user['followers_count'] if 'followers_count' in user else 0,
                following_count=user['friends_count'] if 'friends_count' in user else 0,
                listed_in_count=user['listed_count'] if 'listed_count' in user else 0,
                is_verified=user['verified'] if 'verified' in user else False
            )

            if (tweet['retweet_count'] and tweet['favorite_count'] and
                    (author.get_weight() > 1000 or tweet['entities']['urls'])):
                # Some debug prints, visual confirmation :)
                print '-=' * 45
                print tweet['text'].encode('ascii', 'ignore')
                print tweet['created_at'], tweet['favorite_count'], tweet['retweet_count'], author.get_weight()

                try:
                    author.save()
                except IntegrityError:
                    author = Account.objects.get(twitter_id=user['id_str'])

                mentions = list()

                if tweet['entities']['user_mentions']:
                    for user in tweet['entities']['user_mentions']:
                        try:
                            (mention, created) = Account.objects.get_or_create(
                                twitter_id=user['id_str'],
                                screen_name=user['screen_name'],
                                name=user['name'],
                                url=user['url'] if 'url' in user else None,
                                status_count=user['statuses_count'] if 'statuses_count' in user else 0,
                                follower_count=user['followers_count'] if 'followers_count' in user else 0,
                                following_count=user['friends_count'] if 'friends_count' in user else 0,
                                listed_in_count=user['listed_count'] if 'listed_count' in user else 0,
                                is_verified=user['verified'] if 'verified' in user else False
                            )
                        except IntegrityError:
                            mention = Account.objects.get(twitter_id=user['id_str'])
                        mentions.append(mention)

                try:
                    (tw, created) = Tweet.objects.get_or_create(
                        author=author,
                        text=tweet['text'],
                        tweet_id=tweet['id_str'],
                        created_at=parser.parse(tweet['created_at']),
                        favorite_count=tweet['favorite_count'],
                        retweet_count=tweet['retweet_count']
                    )
                except IntegrityError:
                    tw = Tweet.objects.get(tweet_id=tweet['id_str'])
                for user in mentions:
                    tw.mentions.add(user)
            else:
                continue