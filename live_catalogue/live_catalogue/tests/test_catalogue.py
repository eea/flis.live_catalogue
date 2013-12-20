from os import path
from mock import patch

from .base import (
    BaseWebTest,
    temporary_media_root,
    user_admin_mock
)

from .factories import (
    CategoryFactory,
    FlisTopicFactory,
    NeedFactory
)

from live_catalogue.models import Document


class CatalogueTests(BaseWebTest):

    def setUp(self):
        self.category = CategoryFactory()
        self.flis_topic = FlisTopicFactory()

    @patch('eea_frame.middleware.requests')
    def test_need_add(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
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
            status='open',
            draft=False,
        )

    @patch('eea_frame.middleware.requests')
    def test_need_in_entries_list(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        NeedFactory(categories=[self.category], flis_topics=[self.flis_topic],
                    user_id='johndoe')
        url = self.reverse('home')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.need')
        self.assertEqual(1, len(row))
        self.assertEqual('Catalogue', row.find('td').eq(1).text())

    @patch('eea_frame.middleware.requests')
    def test_need_draft_not_in_entries_list(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        NeedFactory(categories=[self.category], flis_topics=[self.flis_topic],
                    user_id='johndoe', draft=True)
        url = self.reverse('home')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.need')
        self.assertEqual(0, len(row))

    @patch('eea_frame.middleware.requests')
    def test_need_in_my_entries(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        NeedFactory(user_id='john.doe')
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

        url = self.reverse('my_entries')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.need')
        self.assertEqual(1, len(row))
        self.assertEqual('Catalogue', row.find('td').eq(1).text())

    @patch('eea_frame.middleware.requests')
    def test_need_not_in_my_entries(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        NeedFactory(categories=[self.category], flis_topics=[self.flis_topic],
                    user_id='johndoe')
        url = self.reverse('my_entries')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        row = resp.pyquery('.table tbody').find('.need')
        self.assertEqual(0, len(row))

    @patch('eea_frame.middleware.requests')
    def test_need_add_draft(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
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
        self.assertObjectInDatabase(
            model='Catalogue',
            pk=1,
            categories__exact=self.category,
            flis_topics__exact=self.flis_topic,
            draft=True,
            status='draft'
        )

    @patch('eea_frame.middleware.requests')
    def test_need_from_draft_to_open(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        need = NeedFactory(categories=[self.category],
                           flis_topics=[self.flis_topic],
                           user_id='admin',
                           draft=True,
                           status='draft')
        need_data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
            'status': 'draft'
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
            draft=False,
            status='open',
        )

    @patch('eea_frame.middleware.requests')
    def test_need_delete(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        NeedFactory(user_id='admin')
        url = self.reverse('catalogue_delete', kind='need', pk=1)
        self.app.delete(url)
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase('Catalogue', pk=1)

    @patch('eea_frame.middleware.requests')
    def test_need_upload_file_on_edit(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        need = NeedFactory(categories=[self.category],
                           flis_topics=[self.flis_topic],
                           user_id='admin')
        data = NeedFactory.attributes(extra={
            'categories': [self.category],
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

    @patch('eea_frame.middleware.requests')
    def test_document_delete(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
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

    @patch('eea_frame.middleware.requests')
    def test_need_delete_also_deletes_documents(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
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
