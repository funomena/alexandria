# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datastore', '0009_keeprules'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='KeepRules',
            new_name='KeepRule',
        ),
    ]
