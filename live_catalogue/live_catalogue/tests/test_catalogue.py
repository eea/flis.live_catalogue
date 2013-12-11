from mock import patch

from .base import (
    BaseWebTest,
    user_admin_mock
)

from .factories import (
    CategoryFactory,
    FlisTopicFactory,
    NeedFactory
)


class CatalogueTests(BaseWebTest):

    def setUp(self):
        self.category = CategoryFactory()
        self.flis_topic = FlisTopicFactory()

    @patch('eea_frame.middleware.requests')
    def test_need_add(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        data = NeedFactory.attributes(extra={
            'category': self.category,
            'flis_topic': self.flis_topic,
            'need_urgent': True,
        })
        url = self.reverse('catalogue_add', kind='need')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        form = resp.forms['catalogue-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase('Catalogue', pk=1,
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
            kind='need'
        )
