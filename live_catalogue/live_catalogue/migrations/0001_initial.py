# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'live_catalogue_category', (
            ('handle', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'live_catalogue', ['Category'])

        # Adding model 'FlisTopic'
        db.create_table(u'live_catalogue_flistopic', (
            ('handle', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'live_catalogue', ['FlisTopic'])

        # Adding model 'Theme'
        db.create_table(u'live_catalogue_theme', (
            ('handle', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'live_catalogue', ['Theme'])

        # Adding model 'Catalogue'
        db.create_table(u'live_catalogue_catalogue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='open', max_length=32, blank=True)),
            ('type_of', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('resources', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('need_urgent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_person', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=64, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'live_catalogue', ['Catalogue'])

        # Adding M2M table for field categories on 'Catalogue'
        m2m_table_name = db.shorten_name(u'live_catalogue_catalogue_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('catalogue', models.ForeignKey(orm[u'live_catalogue.catalogue'], null=False)),
            ('category', models.ForeignKey(orm[u'live_catalogue.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['catalogue_id', 'category_id'])

        # Adding M2M table for field flis_topics on 'Catalogue'
        m2m_table_name = db.shorten_name(u'live_catalogue_catalogue_flis_topics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('catalogue', models.ForeignKey(orm[u'live_catalogue.catalogue'], null=False)),
            ('flistopic', models.ForeignKey(orm[u'live_catalogue.flistopic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['catalogue_id', 'flistopic_id'])

        # Adding M2M table for field themes on 'Catalogue'
        m2m_table_name = db.shorten_name(u'live_catalogue_catalogue_themes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('catalogue', models.ForeignKey(orm[u'live_catalogue.catalogue'], null=False)),
            ('theme', models.ForeignKey(orm[u'live_catalogue.theme'], null=False))
        ))
        db.create_unique(m2m_table_name, ['catalogue_id', 'theme_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'live_catalogue_category')

        # Deleting model 'FlisTopic'
        db.delete_table(u'live_catalogue_flistopic')

        # Deleting model 'Theme'
        db.delete_table(u'live_catalogue_theme')

        # Deleting model 'Catalogue'
        db.delete_table(u'live_catalogue_catalogue')

        # Removing M2M table for field categories on 'Catalogue'
        db.delete_table(db.shorten_name(u'live_catalogue_catalogue_categories'))

        # Removing M2M table for field flis_topics on 'Catalogue'
        db.delete_table(db.shorten_name(u'live_catalogue_catalogue_flis_topics'))

        # Removing M2M table for field themes on 'Catalogue'
        db.delete_table(db.shorten_name(u'live_catalogue_catalogue_themes'))


    models = {
        u'live_catalogue.catalogue': {
            'Meta': {'object_name': 'Catalogue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['live_catalogue.Category']", 'symmetrical': 'False'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'flis_topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['live_catalogue.FlisTopic']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'need_urgent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'resources': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '32', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'themes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['live_catalogue.Theme']", 'symmetrical': 'False', 'blank': 'True'}),
            'type_of': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'live_catalogue.category': {
            'Meta': {'object_name': 'Category'},
            'handle': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'live_catalogue.flistopic': {
            'Meta': {'object_name': 'FlisTopic'},
            'handle': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'live_catalogue.theme': {
            'Meta': {'object_name': 'Theme'},
            'handle': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['live_catalogue']