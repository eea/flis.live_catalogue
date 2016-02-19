# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('live_catalogue', '0003_auto_20160217_1906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flistopic',
            options={'ordering': ('sort_id',)},
        ),
        migrations.AddField(
            model_name='flistopic',
            name='sort_id',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
