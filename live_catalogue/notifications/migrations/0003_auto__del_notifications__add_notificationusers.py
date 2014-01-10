# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Notifications'
        db.delete_table(u'notifications_notifications')

        # Adding model 'NotificationUsers'
        db.create_table(u'notifications_notificationusers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'notifications', ['NotificationUsers'])


    def backwards(self, orm):
        # Adding model 'Notifications'
        db.create_table(u'notifications_notifications', (
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'notifications', ['Notifications'])

        # Deleting model 'NotificationUsers'
        db.delete_table(u'notifications_notificationusers')


    models = {
        u'notifications.notificationusers': {
            'Meta': {'object_name': 'NotificationUsers'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['notifications']