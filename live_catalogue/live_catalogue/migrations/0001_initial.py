# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Catalogue'
        db.create_table(u'live_catalogue_catalogue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('created_by', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('flis_topic', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('themes', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('resources', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('need_urgent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_person', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=64, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'live_catalogue', ['Catalogue'])

        # Adding model 'CataloguePermission'
        db.create_table(u'live_catalogue_cataloguepermission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('catalogue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='permissions', to=orm['live_catalogue.Catalogue'])),
            ('permission', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'live_catalogue', ['CataloguePermission'])


    def backwards(self, orm):
        # Deleting model 'Catalogue'
        db.delete_table(u'live_catalogue_catalogue')

        # Deleting model 'CataloguePermission'
        db.delete_table(u'live_catalogue_cataloguepermission')


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
            'themes': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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