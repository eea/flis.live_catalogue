import shutil
from tempfile import mkdtemp
from contextlib import contextmanager

from django.db.models import Model
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.test.utils import override_settings

from mock import Mock
from django_webtest import WebTest
from webtest.forms import Select, MultipleSelect
from webtest import AppError


USER_ADMIN_DATA = {
    'user_id': 'admin',
    'user_roles': ['Administrator'],
    'groups': []
}
USER_ANONYMOUS_DATA = {
    'user_id': 'anonymous',
    'user_roles': ['Anonymous'],
    'groups': []
}
USER_NFP_DATA = {
    'user_id': 'john',
    'user_roles': [],
    'groups': [['eionet-nfp', 'NFP'], ['eionet-nfp-cc', 'NFP CC'],
               ['eionet-nfp-cc-al', 'Albania']]
}
USER_NRC_DATA = {
    'user_id': 'john',
    'user_roles': [],
    'groups': [['eionet-nrc-forwardlooking', 'NRC Fowardlooking'],
               ['eionet-nrc-forwardlooking-cc', 'NRC Fowardlooking CC'],
               ['eionet-nrc-forwardlooking-mc', 'NRC Fowardlooking MC']]
}


user_admin_mock = Mock(status_code=200, json=lambda: USER_ADMIN_DATA)
user_nfp_mock = Mock(status_code=200, json=lambda: USER_NFP_DATA)
user_nrc_mock = Mock(status_code=200, json=lambda: USER_NRC_DATA)
user_anonymous_user = Mock(status_code=200, json=lambda: USER_ANONYMOUS_DATA)


class BaseWebTest(WebTest):

    csrf_checks = False

    def __init__(self, *args, **kwargs):
        self.AppError = AppError
        super(BaseWebTest, self).__init__(*args, **kwargs)

    def populate_fields(self, form, data):
        for field_name, field in form.field_order:
            if field_name in data:
                value = data[field_name]
                if isinstance(value, Model):
                    value = value.pk
                if isinstance(field, MultipleSelect):
                    if not isinstance(value, list):
                        value = [value]
                if isinstance(field, (Select, MultipleSelect)):
                    field.force_value(value)
                else:
                    field.value = value
        return form

    def normalize_data(self, data):

        def convert_model_to_pk(value):
            if isinstance(value, Model):
                return value.pk
            return value

        new_data = dict(data)
        for k, v in new_data.items():
            if isinstance(v, list):
                new_data[k] = map(convert_model_to_pk, v)
            else:
                new_data[k] = convert_model_to_pk(v)
        return new_data

    def reverse(self, view_name, *args, **kwargs):
        return reverse(view_name, args=args, kwargs=kwargs)

    def assertObjectInDatabase(self, model, **kwargs):
        if isinstance(model, basestring):
            Model = get_model('live_catalogue', model)
        else:
            Model = model

        if not Model:
            self.fail('Model {} does not exist'.format(model))
        try:
            return Model.objects.get(**kwargs)
        except Model.DoesNotExist:
            self.fail('Object "{}" with kwargs {} does not exist'.format(
                model, str(kwargs)
            ))


@contextmanager
def temporary_media_root():
    tmpdir = mkdtemp()
    try:
        with override_settings(MEDIA_ROOT=tmpdir):
            yield tmpdir
    finally:
        shutil.rmtree(tmpdir)
