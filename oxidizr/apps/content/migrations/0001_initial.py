# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Content'
        db.create_table(u'content_content', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=1000)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000, db_index=True)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=4000, blank=True)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_crawled_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'content', ['Content'])


    def backwards(self, orm):
        # Deleting model 'Content'
        db.delete_table(u'content_content')


    models = {
        u'content.content': {
            'Meta': {'object_name': 'Content'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled_at': ('django.db.models.fields.DateTimeField', [], {}),
            'last_updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '1000'})
        }
    }

    complete_apps = ['content']