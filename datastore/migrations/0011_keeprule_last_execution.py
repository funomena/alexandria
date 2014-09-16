# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datastore', '0010_auto_20140913_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='keeprule',
            name='last_execution',
            field=models.TextField(default=b'NOT RUN'),
            preserve_default=True,
        ),
    ]
