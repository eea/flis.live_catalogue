from xmlrpclib import ServerProxy
from django.conf import settings


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
    pass
