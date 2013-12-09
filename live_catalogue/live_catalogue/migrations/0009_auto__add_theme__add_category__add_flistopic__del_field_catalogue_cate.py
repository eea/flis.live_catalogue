# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Theme'
        db.create_table(u'live_catalogue_theme', (
            ('handle', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'live_catalogue', ['Theme'])

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

        # Deleting field 'Catalogue.category'
        db.delete_column(u'live_catalogue_catalogue', 'category')

        # Deleting field 'Catalogue.theme'
        db.delete_column(u'live_catalogue_catalogue', 'theme')

        # Deleting field 'Catalogue.flis_topic'
        db.delete_column(u'live_catalogue_catalogue', 'flis_topic')

        # Adding M2M table for field category on 'Catalogue'
        m2m_table_name = db.shorten_name(u'live_catalogue_catalogue_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('catalogue', models.ForeignKey(orm[u'live_catalogue.catalogue'], null=False)),
            ('category', models.ForeignKey(orm[u'live_catalogue.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['catalogue_id', 'category_id'])

        # Adding M2M table for field flis_topic on 'Catalogue'
        m2m_table_name = db.shorten_name(u'live_catalogue_catalogue_flis_topic')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('catalogue', models.ForeignKey(orm[u'live_catalogue.catalogue'], null=False)),
            ('flistopic', models.ForeignKey(orm[u'live_catalogue.flistopic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['catalogue_id', 'flistopic_id'])

        # Adding M2M table for field theme on 'Catalogue'
        m2m_table_name = db.shorten_name(u'live_catalogue_catalogue_theme')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('catalogue', models.ForeignKey(orm[u'live_catalogue.catalogue'], null=False)),
            ('theme', models.ForeignKey(orm[u'live_catalogue.theme'], null=False))
        ))
        db.create_unique(m2m_table_name, ['catalogue_id', 'theme_id'])


    def backwards(self, orm):
        # Deleting model 'Theme'
        db.delete_table(u'live_catalogue_theme')

        # Deleting model 'Category'
        db.delete_table(u'live_catalogue_category')

        # Deleting model 'FlisTopic'
        db.delete_table(u'live_catalogue_flistopic')

        # Adding field 'Catalogue.category'
        db.add_column(u'live_catalogue_catalogue', 'category',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)

        # Adding field 'Catalogue.theme'
        db.add_column(u'live_catalogue_catalogue', 'theme',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)

        # Adding field 'Catalogue.flis_topic'
        db.add_column(u'live_catalogue_catalogue', 'flis_topic',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)

        # Removing M2M table for field category on 'Catalogue'
        db.delete_table(db.shorten_name(u'live_catalogue_catalogue_category'))

        # Removing M2M table for field flis_topic on 'Catalogue'
        db.delete_table(db.shorten_name(u'live_catalogue_catalogue_flis_topic'))

        # Removing M2M table for field theme on 'Catalogue'
        db.delete_table(db.shorten_name(u'live_catalogue_catalogue_theme'))


    models = {
        u'live_catalogue.catalogue': {
            'Meta': {'object_name': 'Catalogue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['live_catalogue.Category']", 'symmetrical': 'False'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flis_topic': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['live_catalogue.FlisTopic']", 'symmetrical': 'False'}),
            'geographic_scope': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['live_catalogue.Keyword']", 'null': 'True', 'blank': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'need_urgent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'resources': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'theme': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['live_catalogue.Theme']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'live_catalogue.cataloguepermission': {
            'Meta': {'object_name': 'CataloguePermission'},
            'catalogue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'to': u"orm['live_catalogue.Catalogue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
        u'live_catalogue.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'live_catalogue.theme': {
            'Meta': {'object_name': 'Theme'},
            'handle': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['live_catalogue']