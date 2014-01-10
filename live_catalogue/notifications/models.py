from django.db import models


class Notifications(models.Model):

    user_id = models.CharField(max_length=64, db_index=True)

    def __unicode__(self):
        return self.user_id

