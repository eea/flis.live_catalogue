from os import path

from django import forms
from django.template.defaultfilters import filesizeformat

from live_catalogue.models import Catalogue
from eea_frame.middleware import get_current_request


class FormatString(str):

    def format(self, *args, **kwargs):
        arguments = list(args)
        arguments[1] = path.basename(arguments[1])
        return super(FormatString, self).format(*arguments, **kwargs)


class URLFieldWithTextField(forms.URLField):

    widget = forms.TextInput


class ClearableFileInput(forms.ClearableFileInput):

    template_with_initial = '%(initial)s %(clear_template)s<br />' \
                            '%(input_text)s: %(input)s'

    template_with_clear = '<label class="fix-label">' \
                          '%(clear)s %(clear_checkbox_label)s</label>'

    url_markup_template = FormatString('<a href="{0}">{1}</a> <br>')


class FileUploadRestrictedSize(forms.FileField):
    """
    * max_upload_size - a number indicating the maximum file size allowed for
    upload.
        2.5MB - 2621440
    """
    def __init__(self, *args, **kwargs):
        # default to 2.5MB
        self.max_size = kwargs.pop('max_upload_size', 2621440)
        super(FileUploadRestrictedSize, self).__init__(*args, **kwargs)

    def clean(self, value, *args):
        data = super(FileUploadRestrictedSize, self).clean(value, *args)
        if data:
            file_size = getattr(data.file, '_size', None)
            if file_size and (file_size > self.max_upload_size):
                raise forms.ValidationError(
                    'Please keep filesize under %s. Current filesize %s') % (
                    filesizeformat(self.max_size), filesizeformat(file_size)
                )
        return value


class CatalogueForm(forms.ModelForm):

    REQUIRED_FIELDS = ('subject', 'description', 'status', 'contact_person',
                       'email', 'institution', 'country')

    url = URLFieldWithTextField(required=False)
    document = FileUploadRestrictedSize(required=False,
                                        widget=ClearableFileInput())

    class Meta:

        model = Catalogue
        exclude = ('kind', 'created_by', 'created_on', 'last_updated', 'draft')

        widgets = {
            'address': forms.Textarea(),
        }
        labels = {
            'type_of': 'Type of need',
            'need_urgent': 'Is this need urgent?',
        }

    def __init__(self, *args, **kwargs):
        self.is_draft = kwargs.pop('is_draft', False)
        request = get_current_request()
        self.user_id = request.user_id
        super(CatalogueForm, self).__init__(*args, **kwargs)

        self.fields['status'].empty_label = None
        self.fields['status'].choices = self.fields['status'].choices[1:]

        if self.is_draft is False:
            for f in self.REQUIRED_FIELDS:
                self.fields[f].required = True

    def save(self):
        catalogue = super(CatalogueForm, self).save(commit=False)
        catalogue.kind = self.KIND
        catalogue.draft = self.is_draft
        catalogue.user_id = self.user_id

        catalogue.subject = self.cleaned_data['subject']
        catalogue.description = self.cleaned_data['description']
        catalogue.type_of = self.cleaned_data['type_of']

        if self.is_draft:
            catalogue.status = Catalogue.DRAFT
        else:
            status = self.cleaned_data['status']
            if status == Catalogue.DRAFT:
                catalogue.status = Catalogue.OPEN
            else:
                catalogue.status = status

        catalogue.contact_person = self.cleaned_data['contact_person']
        catalogue.email = self.cleaned_data['email']
        catalogue.phone_number = self.cleaned_data['phone_number']
        catalogue.institution = self.cleaned_data['institution']
        catalogue.address = self.cleaned_data['address']
        catalogue.country = self.cleaned_data['country']
        catalogue.url = self.cleaned_data['url']
        catalogue.info = self.cleaned_data['info']
        document = self.cleaned_data['document']
        if document:
            catalogue.document = document
        else:
            catalogue.document = None
        catalogue.save()

        categories = self.cleaned_data['categories']
        flis_topics = self.cleaned_data['flis_topics']
        themes = self.cleaned_data['themes']

        if categories:
            catalogue.categories.add(*[i for i in categories])
        if flis_topics:
            catalogue.flis_topics.add(*[i for i in flis_topics])
        if themes:
            catalogue.themes.add(*[i for i in themes])

        return catalogue


class NeedForm(CatalogueForm):

    KIND = 'need'

    class Meta(CatalogueForm.Meta):

        exclude = CatalogueForm.Meta.exclude + ('resources',)
        labels = {
            'type_of': 'Type of need',
            'need_urgent': 'Is this need urgent?',
        }

    def save(self):
        catalogue = super(NeedForm, self).save()
        catalogue.need_urgent = self.cleaned_data['need_urgent']
        catalogue.save()
        return catalogue


class OfferForm(CatalogueForm):

    KIND = 'offer'

    class Meta(CatalogueForm.Meta):

        exclude = CatalogueForm.Meta.exclude + ('need_urgent',)
        labels = {
            'type_of': 'Type of offer',
        }

    def save(self):
        catalogue = super(OfferForm, self).save()
        catalogue.resources = self.cleaned_data['resources']
        catalogue.save()
        return catalogue


class CatalogueFilterForm(forms.Form):

    KIND_CHOICES = (('all', 'All'),) + Catalogue.KIND_CHOICES

    kind = forms.ChoiceField(choices=KIND_CHOICES)
