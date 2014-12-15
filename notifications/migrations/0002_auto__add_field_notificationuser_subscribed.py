# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NotificationUser.subscribed'
        db.add_column(u'notifications_notificationuser', 'subscribed',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NotificationUser.subscribed'
        db.delete_column(u'notifications_notificationuser', 'subscribed')


    models = {
        u'notifications.notificationuser': {
            'Meta': {'object_name': 'NotificationUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['notifications']
