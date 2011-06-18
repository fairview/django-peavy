# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LogRecord'
        db.create_table('peavy_logrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('application', self.gf('django.db.models.fields.CharField')(default='?', max_length=256, db_index=True)),
            ('origin_server', self.gf('django.db.models.fields.CharField')(default='?', max_length=256, db_index=True)),
            ('client_ip', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, blank=True)),
            ('user', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=256, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=256, blank=True)),
            ('logger', self.gf('django.db.models.fields.CharField')(max_length=1024, db_index=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('message', self.gf('django.db.models.fields.TextField')(db_index=True)),
            ('stack_trace', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('debug_page', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('peavy', ['LogRecord'])


    def backwards(self, orm):
        
        # Deleting model 'LogRecord'
        db.delete_table('peavy_logrecord')


    models = {
        'peavy.logrecord': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'LogRecord'},
            'application': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '256', 'db_index': 'True'}),
            'client_ip': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'blank': 'True'}),
            'debug_page': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'logger': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'origin_server': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '256', 'db_index': 'True'}),
            'stack_trace': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '256', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '256', 'blank': 'True'})
        }
    }

    complete_apps = ['peavy']
