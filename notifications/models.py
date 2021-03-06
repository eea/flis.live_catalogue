from django.db import models
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse
from django.dispatch import Signal
from django.conf import settings

from .utils import get_user_email


class NotificationUser(models.Model):

    user_id = models.CharField(max_length=64, unique=True)
    subscribed = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user_id + ' ' + ('subscribed' if self.subscribed else '')

    @classmethod
    def send(cls, sender, event_type, request, **kwargs):
        catalogue = sender
        from_email = settings.FROM_EMAIL

        if event_type == 'published':
            action = 'added'
            subject = 'A new {0} was {1}'.format(catalogue.kind, action)
        if event_type == 'updated':
            action = 'edited'
            article = 'An' if catalogue.kind == 'offer' else 'A'
            subject = '{0} {1} was {2}'.format(article, catalogue.kind, action)

        catalogue_url = reverse('catalogue_view', kwargs={
            'pk': catalogue.pk, 'kind': catalogue.kind
        })
        notifications_url = reverse('notifications:home')

        body = render_to_string('notification_email.html', {
            'catalogue': catalogue,
            'action': action,
            'notifications_url': request.build_absolute_uri(notifications_url),
            'catalogue_url': request.build_absolute_uri(catalogue_url),
        })

        datatuple = []
        for user in cls.objects.filter(subscribed=True):
            email = [get_user_email(user.user_id)]
            datatuple.append((subject, body, from_email, email))
        send_mass_mail(datatuple)


catalogue_update_signal = Signal(providing_args=('event_type', 'request'))
catalogue_update_signal.connect(NotificationUser.send)
