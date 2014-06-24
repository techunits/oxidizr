from django.contrib import admin

from .models import Tweet, Handle, Keyword


class KeywordAdmin(admin.ModelAdmin):
    list_display = ['term']
    list_filter = ['term']


admin.site.register(Keyword, KeywordAdmin)


class TweetAdmin(admin.ModelAdmin):
    def author_weight(self, instance):
        return instance.author.weight
    author_weight.short_description = 'Author\'s weight'

    list_display = ['text', 'view_tweet', 'favorite_count', 'retweet_count', 'created_at', 'weight', 'author_weight']


admin.site.register(Tweet, TweetAdmin)


class HandleAdmin(admin.ModelAdmin):
    list_display = ['screen_name', 'status_count', 'follower_count', 'following_count',
                    'listed_in_count', 'is_verified', 'weight']


admin.site.register(Handle, HandleAdmin)