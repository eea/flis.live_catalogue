from django.db import models
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail
from django.dispatch import Signal
from django.template import RequestContext

from .utils import get_user_email


class NotificationUser(models.Model):

    SUBJECT = 'Catalogue entry %s'
    FROM_EMAIL = 'uns@eionet.europa.eu'

    user_id = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.user_id

    @classmethod
    def send(cls, sender, event_type, request, **kwargs):
        catalogue = sender
        body = render_to_string('notification.html', {
            'catalogue': catalogue,
            'event_type': event_type,
        }, context_instance=RequestContext(request))
        datatuple = []
        for user in cls.objects.all():
            email = get_user_email(user.user_id)
            datatuple.append((cls.SUBJECT % event_type, body, cls.FROM_EMAIL,
                             [email]))
        send_mass_mail(datatuple)


catalogue_update_signal = Signal(providing_args=('event_type', 'request'))
catalogue_update_signal.connect(NotificationUser.send)
