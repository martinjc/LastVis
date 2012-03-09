# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('lastfmdata_image')

        # Adding model 'CacheEntry'
        db.create_table('lastfmdata_cacheentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lastfmdata', ['CacheEntry'])


    def backwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('lastfmdata_image', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('lastfmdata', ['Image'])

        # Deleting model 'CacheEntry'
        db.delete_table('lastfmdata_cacheentry')


    models = {
        'lastfmdata.cacheentry': {
            'Meta': {'object_name': 'CacheEntry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lastfmdata']
