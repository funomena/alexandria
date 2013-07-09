# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Artifact.is_secure'
        db.add_column(u'datastore_artifact', 'is_secure',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Artifact.secure_uuid'
        db.add_column(u'datastore_artifact', 'secure_uuid',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True),
                      keep_default=False)


        # Changing field 'Artifact.download_url'
        db.alter_column(u'datastore_artifact', 'download_url', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

    def backwards(self, orm):
        # Deleting field 'Artifact.is_secure'
        db.delete_column(u'datastore_artifact', 'is_secure')

        # Deleting field 'Artifact.secure_uuid'
        db.delete_column(u'datastore_artifact', 'secure_uuid')


        # User chose to not deal with backwards NULL issues for 'Artifact.download_url'
        raise RuntimeError("Cannot reverse this migration. 'Artifact.download_url' and its values cannot be restored.")

    models = {
        u'datastore.artifact': {
            'Meta': {'object_name': 'Artifact'},
            'a_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': u"orm['datastore.ArtifactType']"}),
            'build': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'artifacts'", 'to': u"orm['datastore.Build']"}),
            'download_url': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_secure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'secure_uuid': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'})
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 9, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['datastore']