# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tweet.weight'
        db.alter_column(u'twitter_tweet', 'weight', self.gf('django.db.models.fields.PositiveIntegerField')())

    def backwards(self, orm):

        # Changing field 'Tweet.weight'
        db.alter_column(u'twitter_tweet', 'weight', self.gf('django.db.models.fields.FloatField')())

    models = {
        u'twitter.handle': {
            'Meta': {'object_name': 'Handle'},
            'follower_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'following_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'listed_in_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'status_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        u'twitter.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'twitter.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'statuses'", 'to': u"orm['twitter.Handle']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'favorite_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mentions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': u"orm['twitter.Handle']"}),
            'retweet_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['twitter']