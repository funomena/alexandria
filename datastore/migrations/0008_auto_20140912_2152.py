# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datastore', '0007_auto_20140912_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='allowed_groups',
            field=models.ManyToManyField(to=b'auth.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='build',
            name='tags',
            field=models.ManyToManyField(related_name=b'builds', to=b'datastore.Tag', blank=True),
        ),
    ]
