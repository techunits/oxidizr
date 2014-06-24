# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Handle'
        db.create_table(u'twitter_handle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('twitter_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=254, blank=True)),
            ('status_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('follower_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('following_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('listed_in_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'twitter', ['Handle'])

        # Adding model 'Tweet'
        db.create_table(u'twitter_tweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='statuses', to=orm['twitter.Handle'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('tweet_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('favorite_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('retweet_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'twitter', ['Tweet'])

        # Adding M2M table for field mentions on 'Tweet'
        m2m_table_name = db.shorten_name(u'twitter_tweet_mentions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tweet', models.ForeignKey(orm[u'twitter.tweet'], null=False)),
            ('handle', models.ForeignKey(orm[u'twitter.handle'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tweet_id', 'handle_id'])


    def backwards(self, orm):
        # Deleting model 'Handle'
        db.delete_table(u'twitter_handle')

        # Deleting model 'Tweet'
        db.delete_table(u'twitter_tweet')

        # Removing M2M table for field mentions on 'Tweet'
        db.delete_table(db.shorten_name(u'twitter_tweet_mentions'))


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
            'twitter_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
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
            'tweet_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['twitter']