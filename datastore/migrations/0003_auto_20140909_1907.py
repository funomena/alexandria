# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datastore', '0002_auto_20140904_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artifact',
            name='s3_key',
            field=models.CharField(unique=True, max_length=64),
        ),
    ]
