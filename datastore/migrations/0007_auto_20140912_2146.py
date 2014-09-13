# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datastore', '0006_autoaccessrule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoaccessrule',
            name='required_metadata',
            field=models.ManyToManyField(to=b'datastore.MetadataValue', blank=True),
        ),
        migrations.AlterField(
            model_name='autoaccessrule',
            name='required_tags',
            field=models.ManyToManyField(to=b'datastore.Tag', blank=True),
        ),
    ]
