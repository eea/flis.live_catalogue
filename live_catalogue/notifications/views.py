from xmlrpclib import ServerProxy
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.timezone import localtime
from notifications.definitions import RDF_URI


def get_uns_proxy():
    url = 'http://{0}:{1}@uns.eionet.europa.eu/rpcrouter'.format(
        settings.UNS_LOGIN_USERNAME,
        settings.UNS_LOGIN_PASSWORD)
    return ServerProxy(url).UNSService


def create_channel(title, description=''):
    uns = get_uns_proxy()
    print uns.createChannel(title, description)


def subscribe(user_id):
    uns = get_uns_proxy()
    uns.makeSubscription(settings.UNS_CHANNEL_ID, user_id, [])


def prepare_notification_rdf(item, event_type):
    title = item.subject
    url = reverse('catalogue_view', kwargs={'pk': item.pk, 'kind': item.kind})
    identifier = settings.HOSTNAME + url
    date = localtime(item.created_on).strftime('Y-%b-%d %H:%M:%S')
    actor = item.user_id
    event_data = [
        (RDF_URI['rdf_type'], RDF_URI['catalogue_event']),
        (RDF_URI['title'], title),
        (RDF_URI['identifier'], identifier),
        (RDF_URI['date'], date),
        (RDF_URI['actor'], actor),
        (RDF_URI['actor_name'], actor),
        (RDF_URI['event_type'], event_type),
    ]
    return [[url, pred, obj] for pred, obj in event_data]


def notify(item, event_type):
    send_notification(prepare_notification_rdf(item, event_type))


def send_notification(rdf_triples):
    channel_id = settings.UNS_CHANNEL_ID
    send_notifications = getattr(settings, 'UNS_SUPPRESS_NOTIFICATIONS', False)
    if send_notifications:
        # log.info("Notification via UNS for %s", rdf_triples[0][0])
        # log.debug("Notification data: %r", rdf_triples)
        uns = get_uns_proxy()
        # uns.sendNotification(channel_id, rdf_triples)
    else:
        # log.info("Notification via UNS for %s (not sent)", rdf_triples[0][0])
        pass
    # uns_notification_sent.send(app, rdf_triples=rdf_triples)
