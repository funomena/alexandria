# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datastore', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artifact',
            old_name='secure_uuid',
            new_name='s3_key',
        ),
        migrations.RemoveField(
            model_name='artifact',
            name='is_secure',
        ),
        migrations.RemoveField(
            model_name='artifact',
            name='public_url',
        ),
        migrations.AddField(
            model_name='artifact',
            name='file_size',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='artifact',
            name='md5_hash',
            field=models.CharField(max_length=32, null=True),
            preserve_default=True,
        ),
    ]
