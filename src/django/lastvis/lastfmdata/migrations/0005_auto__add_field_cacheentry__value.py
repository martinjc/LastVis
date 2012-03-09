# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CacheEntry._value'
        db.add_column('lastfmdata_cacheentry', '_value', self.gf('django.db.models.fields.TextField')(null=True, db_column='value', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'CacheEntry._value'
        db.delete_column('lastfmdata_cacheentry', 'value')


    models = {
        'lastfmdata.cacheentry': {
            'Meta': {'object_name': 'CacheEntry'},
            '_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'value'", 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['lastfmdata']
