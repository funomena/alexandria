# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Build'
        db.create_table(u'datastore_build', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'datastore', ['Build'])

        # Adding model 'MetaDataCategory'
        db.create_table(u'datastore_metadatacategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('is_extra_data', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'datastore', ['MetaDataCategory'])

        # Adding model 'MetaData'
        db.create_table(u'datastore_metadata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datastore.MetaDataCategory'])),
            ('build', self.gf('django.db.models.fields.related.ForeignKey')(related_name='metadata', to=orm['datastore.Build'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'datastore', ['MetaData'])

        # Adding model 'ArtifactType'
        db.create_table(u'datastore_artifacttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('is_installer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('download_decorator', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'datastore', ['ArtifactType'])

        # Adding model 'Artifact'
        db.create_table(u'datastore_artifact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('a_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['datastore.ArtifactType'])),
            ('build', self.gf('django.db.models.fields.related.ForeignKey')(related_name='artifacts', to=orm['datastore.Build'])),
            ('download_url', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'datastore', ['Artifact'])


    def backwards(self, orm):
        # Deleting model 'Build'
        db.delete_table(u'datastore_build')

        # Deleting model 'MetaDataCategory'
        db.delete_table(u'datastore_metadatacategory')

        # Deleting model 'MetaData'
        db.delete_table(u'datastore_metadata')

        # Deleting model 'ArtifactType'
        db.delete_table(u'datastore_artifacttype')

        # Deleting model 'Artifact'
        db.delete_table(u'datastore_artifact')


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
            'download_decorator': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_installer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'datastore.build': {
            'Meta': {'object_name': 'Build'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'datastore.metadata': {
            'Meta': {'object_name': 'MetaData'},
            'build': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata'", 'to': u"orm['datastore.Build']"}),
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