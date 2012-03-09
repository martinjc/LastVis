# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'CacheEntry.value'
        db.delete_column('lastfmdata_cacheentry', 'value')


    def backwards(self, orm):
        
        # Adding field 'CacheEntry.value'
        db.add_column('lastfmdata_cacheentry', 'value', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    models = {
        'lastfmdata.cacheentry': {
            'Meta': {'object_name': 'CacheEntry'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['lastfmdata']
