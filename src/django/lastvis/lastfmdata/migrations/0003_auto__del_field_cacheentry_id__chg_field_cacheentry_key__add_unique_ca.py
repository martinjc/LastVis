# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'CacheEntry.id'
        db.delete_column('lastfmdata_cacheentry', 'id')

        # Changing field 'CacheEntry.key'
        db.alter_column('lastfmdata_cacheentry', 'key', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True))

        # Adding unique constraint on 'CacheEntry', fields ['key']
        db.create_unique('lastfmdata_cacheentry', ['key'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'CacheEntry', fields ['key']
        db.delete_unique('lastfmdata_cacheentry', ['key'])

        # Adding field 'CacheEntry.id'
        db.add_column('lastfmdata_cacheentry', 'id', self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True), keep_default=False)

        # Changing field 'CacheEntry.key'
        db.alter_column('lastfmdata_cacheentry', 'key', self.gf('django.db.models.fields.CharField')(max_length=32))


    models = {
        'lastfmdata.cacheentry': {
            'Meta': {'object_name': 'CacheEntry'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lastfmdata']
