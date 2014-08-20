# -*- coding: utf-8 -*-

from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.text import slugify

from live_catalogue.models import Catalogue, Document, Category
from eea_frame.middleware import get_current_request


class URLFieldWithTextField(forms.URLField):

    widget = forms.TextInput


class FileUploadRestrictedSize(forms.FileField):

    def __init__(self, *args, **kwargs):
        # default to 2.5MB
        self.max_size = kwargs.pop('max_upload_size', 2621440)
        super(FileUploadRestrictedSize, self).__init__(*args, **kwargs)

    def clean(self, value, *args):
        data = super(FileUploadRestrictedSize, self).clean(value, *args)
        if not data:
            return value

        file_size = getattr(data, '_size', None)
        if file_size and (file_size > self.max_size):
            raise forms.ValidationError(
                'Please keep filesize under %s. Current filesize %s' % (
                    filesizeformat(self.max_size),
                    filesizeformat(file_size)
                )
            )
        return value


class DocumentForm(forms.ModelForm):

    name = FileUploadRestrictedSize(required=False)

    class Meta:

        model = Document


class BaseDocumentFormset(forms.formsets.BaseFormSet):

    def save(self, catalogue):

        for form in self.forms:
            if not form.cleaned_data:
                continue
            doc = Document.objects.create(name=form.cleaned_data['name'])
            catalogue.documents.add(doc)


class CatalogueForm(forms.ModelForm):

    REQUIRED_FIELDS = ('subject', 'description', 'status', 'contact_person',
                       'email', 'institution', 'country')

    url = URLFieldWithTextField(required=False)

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

        self._set_help_texts()

        self.fields['status'].empty_label = None
        self.fields['status'].choices = self.fields['status'].choices[1:]

        if self.is_draft is False:
            for f in self.REQUIRED_FIELDS:
                self.fields[f].required = True

    def _set_help_texts(self):
        # this function overwrites help_texts because
        # django uses string_concat for help_texts for SelectMultiple fields
        help_texts = getattr(self._meta, 'help_texts', {})
        for key, value in help_texts.items():
            if key in self.fields:
                self.fields[key].help_text = value

    def save(self):
        catalogue = super(CatalogueForm, self).save(commit=False)
        catalogue.kind = self.KIND
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
        help_texts = {
            'categories': 'Enter the type of need you want to add. You may '
                          'select multiple options.',
            'flis_topics': """
                Select the component from the system of Knowledge base for
                <a href="http://www.eea.europa.eu/publications/knowledge-base-for-forward-looking"
                   target="_blank">
                Forward-Looking Information and Services</a> to which the need is
                referring to (you may select multiple options)
            """,
            'themes': """
                The need you are describing is related to forward
                looking information in one (or more) of the EEAs’ topics
                <a href="http://www.eea.europa.eu/themes">
                http://www.eea.europa.eu/themes</a>
            """,
            'subject': 'Title indicating the key essence of the offer',
            'description': 'Describe in a few words what you are needing',
            'type_of': """
                Is the need “official”, by a country or an institution,
                or “informal,” created only for informal cooperation with
                other experts?
            """,
            'contact_person': """
                Contact information of the logged-in user is pre-filled
                automatically from the EIONET directory. It can be edited.
            """,
            'documents': 'Please upload specific files related to the need',
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
        help_texts = {
            'categories': 'Enter the type of offer you want to add. You may '
                          'select multiple options.',
            'flis_topics': """
                Select the component from the system of Knowledge base for
                <a href="http://www.eea.europa.eu/publications/knowledge-base-for-forward-looking"
                   target="_blank">
                Forward-Looking Information and Services</a> to which the offer is
                referring to (you may select multiple options)
            """,
            'themes': """
                The offer you are describing is related to forward looking
                information in one (or more) of the EEAs’ topics  as described
                there:
                <a href="http://www.eea.europa.eu/themes">
                    http://www.eea.europa.eu/themes</a>
            """,
            'subject': 'Title indicating the key essence of the offer',
            'description': 'Describe in a few words what you are offering',
            'type_of': """
                Is the offer “official”, offered by a country or an
                institution, or “informal,” created only for informal
                cooperation with other experts?
            """,
            'resources': """
                Please insert any information related to the offer and use of
                resources: <br>
                - human resources, <br>
                - financial resources, <br>
                - other type of resources.
            """,
            'contact_person': """
                Contact information of the logged-in user is pre-filled
                automatically from the EIONET directory. It can be edited.
            """,
            'documents': 'Please upload specific files related to the offer',
        }

    def save(self):
        catalogue = super(OfferForm, self).save()
        catalogue.resources = self.cleaned_data['resources']
        catalogue.save()
        return catalogue


class CatalogueFilterForm(forms.Form):

    KIND_CHOICES = (('all', 'All'),) + Catalogue.KIND_CHOICES

    kind = forms.ChoiceField(choices=KIND_CHOICES, widget=forms.RadioSelect)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('handle',)

    def save(self, commit=True):
        category = super(CategoryForm, self).save(commit=False)
        if not category.handle:
            category.handle = slugify(category.title)
        if commit:
            category.save()
        return category