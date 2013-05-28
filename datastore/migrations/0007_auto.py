# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field builds on 'MetaData'
        db.delete_table('datastore_metadata_builds')

        # Adding M2M table for field metadata on 'Build'
        db.create_table(u'datastore_build_metadata', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('build', models.ForeignKey(orm[u'datastore.build'], null=False)),
            ('metadata', models.ForeignKey(orm[u'datastore.metadata'], null=False))
        ))
        db.create_unique(u'datastore_build_metadata', ['build_id', 'metadata_id'])


    def backwards(self, orm):
        # Adding M2M table for field builds on 'MetaData'
        db.create_table(u'datastore_metadata_builds', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metadata', models.ForeignKey(orm[u'datastore.metadata'], null=False)),
            ('build', models.ForeignKey(orm[u'datastore.build'], null=False))
        ))
        db.create_unique(u'datastore_metadata_builds', ['metadata_id', 'build_id'])

        # Removing M2M table for field metadata on 'Build'
        db.delete_table('datastore_build_metadata')


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
            'is_extra_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['datastore']