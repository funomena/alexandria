# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExtraDataValue'
        db.create_table(u'datastore_extradatavalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ed_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datastore.ExtraDataType'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('build', self.gf('django.db.models.fields.related.ForeignKey')(related_name='extra_data', to=orm['datastore.Build'])),
        ))
        db.send_create_signal(u'datastore', ['ExtraDataValue'])

        # Adding model 'ExtraDataType'
        db.create_table(u'datastore_extradatatype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'datastore', ['ExtraDataType'])

        # Deleting field 'MetaDataCategory.is_extra_data'
        db.delete_column(u'datastore_metadatacategory', 'is_extra_data')


    def backwards(self, orm):
        # Deleting model 'ExtraDataValue'
        db.delete_table(u'datastore_extradatavalue')

        # Deleting model 'ExtraDataType'
        db.delete_table(u'datastore_extradatatype')

        # Adding field 'MetaDataCategory.is_extra_data'
        db.add_column(u'datastore_metadatacategory', 'is_extra_data',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'datastore.artifact': {
            'Meta': {'object_name': 'Artifact'},
            'a_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': u"orm['datastore.ArtifactType']"}),
            'build': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'artifacts'", 'to': u"orm['datastore.Build']"}),
            'download_url': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'datastore.artifacttype': {
            'Meta': {'object_name': 'ArtifactType'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installer_type': ('django.db.models.fields.CharField', [], {'default': "'NOT INSTALLER'", 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'datastore.build': {
            'Meta': {'object_name': 'Build'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': "'1970-01-01 00:01'", 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'builds'", 'symmetrical': 'False', 'to': u"orm['datastore.MetaData']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'starred': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'datastore.extradatatype': {
            'Meta': {'object_name': 'ExtraDataType'},
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'datastore.extradatavalue': {
            'Meta': {'object_name': 'ExtraDataValue'},
            'build': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extra_data'", 'to': u"orm['datastore.Build']"}),
            'ed_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': u"orm['datastore.ExtraDataType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'datastore.metadata': {
            'Meta': {'object_name': 'MetaData'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': u"orm['datastore.MetaDataCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'datastore.metadatacategory': {
            'Meta': {'object_name': 'MetaDataCategory'},
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['datastore']