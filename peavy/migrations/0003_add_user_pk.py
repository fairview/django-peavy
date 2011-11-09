# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'LogRecord.user_pk'
        db.add_column('peavy_logrecord', 'user_pk', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True), keep_default=False)

        # rename user to username
        db.rename_column('peavy_logrecord', 'user', 'username')


    def backwards(self, orm):
        
        # Deleting field 'LogRecord.user_pk'
        db.delete_column('peavy_logrecord', 'user_pk')

        # rename username back to user
        db.rename_column('peavy_logrecord', 'username', 'user')

    models = {
        'peavy.logrecord': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'LogRecord'},
            'application': ('django.db.models.fields.CharField', [], {'default': "'sandbox'", 'max_length': '256', 'db_index': 'True'}),
            'client_ip': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'blank': 'True'}),
            'debug_page': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'logger': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'origin_server': ('django.db.models.fields.CharField', [], {'default': "'kaze.jkcl.local'", 'max_length': '256', 'db_index': 'True'}),
            'stack_trace': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '256', 'blank': 'True'}),
            'user_pk': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '256', 'blank': 'True'})
        }
    }

    complete_apps = ['peavy']
