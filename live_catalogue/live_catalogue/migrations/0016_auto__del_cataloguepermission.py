# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CataloguePermission'
        db.delete_table(u'live_catalogue_cataloguepermission')


    def backwards(self, orm):
        # Adding model 'CataloguePermission'
        db.create_table(u'live_catalogue_cataloguepermission', (
            ('catalogue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='permissions', to=orm['live_catalogue.Catalogue'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('permission', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'live_catalogue', ['CataloguePermission'])


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
            'flis_topic': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['live_catalogue.FlisTopic']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'need_urgent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'resources': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '10', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'theme': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['live_catalogue.Theme']", 'symmetrical': 'False', 'blank': 'True'}),
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