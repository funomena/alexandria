# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('datastore', '0004_auto_20140910_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='allowed_groups',
            field=models.ManyToManyField(to='auth.Group'),
            preserve_default=True,
        ),
    ]
