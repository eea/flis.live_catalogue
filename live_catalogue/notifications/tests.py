import factory

from django.core import mail
from mock import patch

from live_catalogue.tests.base import BaseWebTest, user_admin_mock
from live_catalogue.tests.factories import (NeedFactory, CategoryFactory,
                                            FlisTopicFactory)
from notifications.models import NotificationUser


class NotificationUserFactory(factory.DjangoModelFactory):

    FACTORY_FOR = NotificationUser

    user_id = 'johndoe'


@patch('eea_frame.middleware.requests')
@patch('notifications.utils.LdapConnection')
class NotificationTest(BaseWebTest):

    def setUp(self):
        self.category = CategoryFactory()
        self.flis_topic = FlisTopicFactory()
        NotificationUserFactory()

    def test_new_entry_triggers_notifications(self, LdapConnectionMock,
                                              mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        ldap_mock.get_user_name.return_value = 'John Doe'
        ldap_mock.get_user_email.return_value = 'john.doe@eaudeweb.ro'
        data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
            'need_urgent': True,
        })
        url = self.reverse('catalogue_add', kind='need')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        form = resp.forms['catalogue-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'A new need was added')
        self.assertEqual(mail.outbox[0].from_email, 'no-reply@eaudeweb.ro')

    def test_edit_entry_triggers_notifications(self, LdapConnectionMock,
                                               mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        ldap_mock.get_user_name.return_value = 'John Doe'
        ldap_mock.get_user_email.return_value = 'john.doe@eaudeweb.ro'
        need = NeedFactory(categories=[self.category],
                           flis_topics=[self.flis_topic],
                           user_id='admin',
                           status='draft')
        data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
            'status': 'open',
        })
        url = self.reverse('catalogue_edit', kind='need', pk=need.pk)
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        form = resp.forms['catalogue-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'A need was edited')
        self.assertEqual(mail.outbox[0].from_email, 'no-reply@eaudeweb.ro')

    def test_draft_entry_does_not_trigger_notifications(self,
                                                        LdapConnectionMock,
                                                        mock_requests):

        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        ldap_mock.get_user_name.return_value = 'John Doe'
        ldap_mock.get_user_email.return_value = 'john.doe@eaudeweb.ro'
        need_factory_data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
        })
        data = {'categories': need_factory_data['categories'],
                'flis_topics': need_factory_data['flis_topics'],
                'status': 'open',
                'save': 'draft',
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MAX_NUM_FORMS': 5}

        url = self.reverse('catalogue_add', kind='need')
        self.app.post(url, self.normalize_data(data)).follow()
        self.assertEqual(len(mail.outbox), 0)


@patch('eea_frame.middleware.requests')
class SubscriptionTests(BaseWebTest):

    def test_subscribe_to_notifications(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        url = self.reverse('notifications:subscribe')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_code)
        self.assertObjectInDatabase(
            model='NotificationUser',
            app='notifications',
            user_id='admin')

    def test_unsubscribe_from_notifications(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        NotificationUserFactory(user_id='admin')
        url = self.reverse('notifications:subscribe')
        resp = self.app.delete(url)
        self.assertEqual(200, resp.status_code)
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase(
                model='NotificationUser',
                app='notifications',
                user_id='admin')
