# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Website'
        db.create_table(u'websites_website', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=155)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_banned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_deep_crawl', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_crawled_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'websites', ['Website'])


    def backwards(self, orm):
        # Deleting model 'Website'
        db.delete_table(u'websites_website')


    models = {
        u'websites.website': {
            'Meta': {'object_name': 'Website'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deep_crawl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_crawled_at': ('django.db.models.fields.DateTimeField', [], {}),
            'last_updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '155'})
        }
    }

    complete_apps = ['websites']