# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datastore', '0003_auto_20140909_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='artifact',
            name='verified',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='artifact',
            name='md5_hash',
            field=models.CharField(max_length=32),
        ),
    ]
