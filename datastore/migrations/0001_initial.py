# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public_url', models.CharField(max_length=128, null=True)),
                ('is_secure', models.BooleanField(default=False)),
                ('secure_uuid', models.CharField(max_length=64, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArtifactCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
                ('friendly_name', models.CharField(max_length=64)),
                ('installer_type', models.CharField(default=b'Not Installer', max_length=32, choices=[(b'Not Installer', b'Not Installer'), (b'Normal Installer', b'Normal Installer'), (b'iPhone Installer', b'iPhone Installer'), (b'Android Installer', b'Android Installer')])),
                ('extension', models.CharField(max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetadataCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friendly_name', models.CharField(max_length=128)),
                ('slug', models.SlugField(unique=True)),
                ('required', models.BooleanField(default=False)),
                ('datatype', models.CharField(default=b'string', max_length=16, choices=[(b'string', b'string'), (b'link', b'link'), (b'integer', b'integer'), (b'datetime', b'datetime')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetadataValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string_value', models.CharField(max_length=256)),
                ('category', models.ForeignKey(related_name=b'values', to='datastore.MetadataCategory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='build',
            name='metadata',
            field=models.ManyToManyField(related_name=b'builds', to='datastore.MetadataValue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='build',
            name='tags',
            field=models.ManyToManyField(related_name=b'builds', to='datastore.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='artifact',
            name='build',
            field=models.ForeignKey(related_name=b'artifacts', to='datastore.Build'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='artifact',
            name='category',
            field=models.ForeignKey(related_name=b'instances', to='datastore.ArtifactCategory'),
            preserve_default=True,
        ),
    ]
