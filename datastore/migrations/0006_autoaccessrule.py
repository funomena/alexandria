# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('datastore', '0005_build_allowed_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoAccessRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('all_access_override', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(to='auth.Group')),
                ('required_metadata', models.ManyToManyField(to='datastore.MetadataValue')),
                ('required_tags', models.ManyToManyField(to='datastore.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
