# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Keyword'
        db.create_table(u'meetup_keyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'meetup', ['Keyword'])

        # Adding model 'Event'
        db.create_table(u'meetup_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('event_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('group_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('photo_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('venue_city', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('venue_country', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'meetup', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Keyword'
        db.delete_table(u'meetup_keyword')

        # Deleting model 'Event'
        db.delete_table(u'meetup_event')


    models = {
        u'meetup.event': {
            'Meta': {'object_name': 'Event'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'event_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'group_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'venue_city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'venue_country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'meetup.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['meetup']