from mock import patch

from .factories import NeedFactory
from .base import (
    BaseWebTest,
    user_nfp_mock,
    user_nrc_mock,
    user_anonymous_user,
)


@patch('frame.middleware.requests')
@patch('notifications.utils.LdapConnection')
class CataloguePermissionTests(BaseWebTest):

    def test_eionet_nfp_has_view_access(self, LdapConnectionMock,
                                        mock_requests):
        mock_requests.get.return_value = user_nfp_mock
        resp = self.app.get(self.reverse('home'))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, resp.pyquery('.table').length)

    def test_eionet_simple_user_does_not_have_access(self, LdapConnectionMock,
                                                     mock_requests):
        mock_requests.get.return_value = user_anonymous_user
        resp = self.app.get(self.reverse('home'))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, resp.pyquery('#restricted-title').length)

    def test_eionet_nrc_forwardlooking_add_access(self, LdapConnectionMock,
                                                  mock_requests):
        mock_requests.get.return_value = user_nrc_mock
        url = self.reverse('catalogue_add', kind='need')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, resp.pyquery('#catalogue-form').length)

    def test_eionet_nfp_does_not_have_add_access(self, LdapConnectionMock,
                                                 mock_requests):
        mock_requests.get.return_value = user_nfp_mock
        url = self.reverse('catalogue_add', kind='need')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, resp.pyquery('#restricted-title').length)

    def test_catalogue_edit_by_the_same_user(self, LdapConnectionMock,
                                             mock_requests):
        mock_requests.get.return_value = user_nrc_mock
        NeedFactory(user_id='john')
        url = self.reverse('catalogue_edit', kind='need', pk=1)
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, resp.pyquery('#catalogue-form').length)

    def test_catalogue_edit_by_a_different_user(self, LdapConnectionMock,
                                                mock_requests):
        mock_requests.get.return_value = user_nrc_mock
        NeedFactory(user_id='jonh.doe')
        url = self.reverse('catalogue_edit', kind='need', pk=1)
        with self.assertRaises(self.AppError):
            self.app.get(url)

    def test_catalogue_delete_by_a_different_user(self, LdapConnectionMock,
                                                  mock_requests):
        mock_requests.get.return_value = user_nrc_mock
        NeedFactory(user_id='jonh.doe')
        url = self.reverse('catalogue_delete', kind='need', pk=1)
        with self.assertRaises(self.AppError):
            self.app.delete(url)
