# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Catalogue.themes'
        db.delete_column(u'live_catalogue_catalogue', 'themes')

        # Adding field 'Catalogue.theme'
        db.add_column(u'live_catalogue_catalogue', 'theme',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Catalogue.themes'
        raise RuntimeError("Cannot reverse this migration. 'Catalogue.themes' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Catalogue.themes'
        db.add_column(u'live_catalogue_catalogue', 'themes',
                      self.gf('django.db.models.fields.CharField')(max_length=64),
                      keep_default=False)

        # Deleting field 'Catalogue.theme'
        db.delete_column(u'live_catalogue_catalogue', 'theme')


    models = {
        u'live_catalogue.catalogue': {
            'Meta': {'object_name': 'Catalogue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'flis_topic': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'need_urgent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'resources': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'live_catalogue.cataloguepermission': {
            'Meta': {'object_name': 'CataloguePermission'},
            'catalogue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'to': u"orm['live_catalogue.Catalogue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['live_catalogue']