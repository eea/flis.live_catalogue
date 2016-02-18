# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('live_catalogue', '0002_catalogue_deadline'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('sort_id',)},
        ),
        migrations.AddField(
            model_name='category',
            name='sort_id',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
