from django.conf.urls import url
from notifications.views import Notifications, Subscribe, NotificationsManager


urlpatterns = [
    url(r'^$', Notifications.as_view(), name='home'),
    url(r'^subscribe$', Subscribe.as_view(), name='subscribe'),
    url(r'^unsubscribe$', Subscribe.as_view(), name='unsubscribe'),
    url(r'^manager$', NotificationsManager.as_view(), name='manager'),
]
