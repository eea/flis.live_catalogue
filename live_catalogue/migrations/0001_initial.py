# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150615_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(db_index=True, max_length=5, choices=[(b'need', b'Need'), (b'offer', b'Offer')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('user_id', models.CharField(max_length=64, blank=True)),
                ('subject', models.CharField(max_length=256, blank=True)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(default=b'open', max_length=32, blank=True, choices=[(b'open', b'Open'), (b'solved', b'Solved'), (b'closed-without-solution', b'Closed without solution'), (b'draft', b'Draft')])),
                ('type_of', models.CharField(blank=True, max_length=10, choices=[(b'official', b'Official'), (b'informal', b'Informal')])),
                ('resources', models.TextField(blank=True)),
                ('need_urgent', models.BooleanField(default=False)),
                ('contact_person', models.CharField(max_length=64, blank=True)),
                ('email', models.EmailField(max_length=64, blank=True)),
                ('phone_number', models.CharField(max_length=64, blank=True)),
                ('institution', models.CharField(max_length=64, blank=True)),
                ('address', models.CharField(max_length=256, blank=True)),
                ('url', models.URLField(blank=True)),
                ('info', models.TextField(verbose_name=b'Additional contact details', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('handle', models.SlugField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.FileField(upload_to=b'documents')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlisTopic',
            fields=[
                ('handle', models.SlugField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='catalogue',
            name='categories',
            field=models.ManyToManyField(to='live_catalogue.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='catalogue',
            name='country',
            field=models.ForeignKey(to='common.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='catalogue',
            name='documents',
            field=models.ManyToManyField(to='live_catalogue.Document', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='catalogue',
            name='flis_topics',
            field=models.ManyToManyField(to='live_catalogue.FlisTopic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='catalogue',
            name='themes',
            field=models.ManyToManyField(to='common.EnvironmentalTheme', verbose_name=b'Topics', blank=True),
            preserve_default=True,
        ),
    ]
