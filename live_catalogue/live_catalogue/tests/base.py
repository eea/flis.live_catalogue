from django.db.models import Model
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model

from mock import Mock
from django_webtest import WebTest
from webtest.forms import Select, MultipleSelect
from webtest import AppError


USER_ADMIN_DATA = {'user_id': 'admin', 'user_roles': ['Administrator'],
                   'groups': []}
user_admin_mock = Mock(status_code=200, json=lambda: USER_ADMIN_DATA)


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
        new_data = dict(data)
        for k, v in new_data.items():
            if isinstance(v, Model):
                new_data[k] = str(v.pk)
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
