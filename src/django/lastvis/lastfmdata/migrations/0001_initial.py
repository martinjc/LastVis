# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('lastfmdata_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('lastfmdata', ['Image'])


    def backwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('lastfmdata_image')


    models = {
        'lastfmdata.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        }
    }

    complete_apps = ['lastfmdata']
