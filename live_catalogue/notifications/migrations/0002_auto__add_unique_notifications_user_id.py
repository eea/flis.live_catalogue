# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Notifications', fields ['user_id']
        db.create_unique(u'notifications_notifications', ['user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Notifications', fields ['user_id']
        db.delete_unique(u'notifications_notifications', ['user_id'])


    models = {
        u'notifications.notifications': {
            'Meta': {'object_name': 'Notifications'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        }
    }

    complete_apps = ['notifications']