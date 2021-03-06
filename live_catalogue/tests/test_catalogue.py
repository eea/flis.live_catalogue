from os import path
from mock import patch

from .base import (
    BaseWebTest,
    temporary_media_root,
    user_admin_mock
)

from .factories import (
    CategoryFactory,
    CountryFactory,
    FlisTopicFactory,
    NeedFactory
)

from live_catalogue.models import Catalogue, Document


@patch('frame.middleware.requests')
@patch('notifications.utils.LdapConnection')
class CatalogueTests(BaseWebTest):

    def setUp(self):
        self.category = CategoryFactory()
        self.flis_topic = FlisTopicFactory()
        self.country = CountryFactory()

    def test_need_add(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
            'need_urgent': True,
            'country': self.country,
        })
        url = self.reverse('catalogue_add', kind='need')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        form = resp.forms['catalogue-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(
            model='Catalogue',
            pk=1,
            categories__exact=self.category.handle,
            flis_topics__exact=self.flis_topic.handle,
            subject=data['subject'],
            description=data['description'],
            contact_person=data['contact_person'],
            email=data['email'],
            url__startswith=data['url'],
            institution=data['institution'],
            country=data['country'],
            need_urgent=True,
            kind='need',
            status=Catalogue.OPEN,
        )

    def test_need_in_entries_list(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        NeedFactory(categories=[self.category], flis_topics=[self.flis_topic],
                    user_id='johndoe', status='open')
        url = self.reverse('home')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.need')
        self.assertEqual(1, len(row))
        self.assertIn('Catalogue', row.find('td').eq(1).text())

    def test_need_draft_not_in_entries_list(self, LdapConnectionMock,
                                            mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        NeedFactory(categories=[self.category], flis_topics=[self.flis_topic],
                    user_id='johndoe', status=Catalogue.DRAFT)
        url = self.reverse('home')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.need')
        self.assertEqual(0, len(row))

    def test_need_in_my_entries(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        NeedFactory(user_id='john.doe')
        data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
            'need_urgent': True,
            'country': self.country,
        })
        url = self.reverse('catalogue_add', kind='need')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        form = resp.forms['catalogue-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()

        url = self.reverse('my_entries')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.need')
        self.assertEqual(1, len(row))
        self.assertIn('Catalogue', row.find('td').eq(1).text())

    def test_need_not_in_my_entries(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        NeedFactory(categories=[self.category], flis_topics=[self.flis_topic],
                    user_id='johndoe')
        url = self.reverse('my_entries')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.need')
        self.assertEqual(0, len(row))

    def test_filter_my_entries(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        NeedFactory(user_id='admin')
        url = self.reverse('my_entries')
        resp = self.app.get(url, params={'kind': 'need'})
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.need')
        self.assertEqual(1, len(row))

        resp = self.app.get(url, params={'kind': 'offer'})
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.offer')
        self.assertEqual(0, len(row))

    def test_need_add_draft(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        need_factory_data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
        })
        data = {'categories': need_factory_data['categories'],
                'flis_topics': need_factory_data['flis_topics'],
                'country': self.country,
                'status': 'draft',
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MAX_NUM_FORMS': 5}
        url = self.reverse('catalogue_add', kind='need')
        self.app.post(url, self.normalize_data(data)).follow()
        self.assertObjectInDatabase(
            model='Catalogue',
            pk=1,
            categories__exact=self.category,
            flis_topics__exact=self.flis_topic,
            status=Catalogue.DRAFT
        )

    def test_need_stays_draft(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        need = NeedFactory(categories=[self.category],
                           flis_topics=[self.flis_topic],
                           user_id='admin',
                           status=Catalogue.DRAFT)
        need_data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'country': self.country,
            'flis_topics': [self.flis_topic],
            'status': Catalogue.DRAFT
        })
        url = self.reverse('catalogue_edit', kind='need', pk=need.pk)
        resp = self.app.get(url)
        form = resp.forms['catalogue-form']
        self.populate_fields(form, self.normalize_data(need_data))
        form.submit().follow()
        self.assertObjectInDatabase(
            model='Catalogue',
            pk=1,
            categories__exact=self.category,
            flis_topics__exact=self.flis_topic,
            status=Catalogue.DRAFT,
        )

    def test_need_delete(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        NeedFactory(user_id='admin')
        url = self.reverse('catalogue_delete', kind='need', pk=1)
        self.app.delete(url)
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase('Catalogue', pk=1)

    def test_need_upload_file_on_edit(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        need = NeedFactory(categories=[self.category],
                           flis_topics=[self.flis_topic],
                           user_id='admin')
        data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'country': self.country,
            'flis_topics': [self.flis_topic],
            'status': 'open',
        })
        url = self.reverse('catalogue_edit', kind='need', pk=need.pk)

        with temporary_media_root() as tmpdir:
            data['form-0-name'] = ('document_1.txt', 'Document')
            resp = self.app.get(url)
            form = resp.forms['catalogue-form']
            self.populate_fields(form, self.normalize_data(data))
            form.submit().follow()
            self.assertObjectInDatabase('Document', pk=1,
                                        name='documents/document_1.txt')
            file_path = path.join(tmpdir, 'documents', 'document_1.txt')
            self.assertTrue(path.exists(file_path))

    def test_document_delete(self, LdapConnectionMock, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        need = NeedFactory(categories=[self.category],
                           flis_topics=[self.flis_topic],
                           user_id='admin')

        with temporary_media_root() as tmpdir:
            doc = Document.objects.create(name='document.txt')
            need.documents.add(doc)
            file_name = path.join(tmpdir, doc.name.name)
            with open(file_name, 'w+'):
                pass

            url = self.reverse('catalogue_document_delete',
                               catalogue_id=need.pk,
                               doc_id=doc.pk)
            resp = self.app.delete(url)
            self.assertEqual(200, resp.status_code)
            self.assertFalse(path.exists(file_name))
            with self.assertRaises(AssertionError):
                self.assertObjectInDatabase('Document', pk=1)

    def test_need_delete_also_deletes_documents(self, LdapConnectionMock,
                                                mock_requests):
        mock_requests.get.return_value = user_admin_mock
        ldap_mock = LdapConnectionMock.return_value
        ldap_mock.get_user_data.return_value = {}
        need = NeedFactory(categories=[self.category],
                           flis_topics=[self.flis_topic],
                           user_id='admin')
        with temporary_media_root() as tmpdir:
            doc = Document.objects.create(name='document.txt')
            need.documents.add(doc)
            file_name = path.join(tmpdir, doc.name.name)
            with open(file_name, 'w+'):
                pass

            url = self.reverse('catalogue_delete', kind='need', pk=1)
            self.app.delete(url)

            self.assertFalse(path.exists(file_name))
            with self.assertRaises(AssertionError):
                self.assertObjectInDatabase('Document', pk=1)
