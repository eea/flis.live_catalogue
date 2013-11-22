from django import forms
from django_select2 import AutoModelSelect2TagField
from live_catalogue.models import Catalogue, Keyword, CataloguePermission
from eea_frame.middleware import get_current_request


class KeywordsField(AutoModelSelect2TagField):

    queryset = Keyword.objects
    search_fields = ('name__icontains',)
    to_field_name = ('name', )

    def get_model_field_values(self, value):
        return {'name': value}


class CatalogueForm(forms.ModelForm):

    NRC_FLIS, EIONET = 'eionet-nrc-forwardlooking', 'eionet'
    PERMS_CHOICES = ((NRC_FLIS, 'NRC Flis'), (EIONET, 'All members of EIONET'),)

    REQUIRED_FIELDS = ('status', 'title', 'keywords', 'start_date',
                       'contact_person', 'email', 'institution', 'country',)

    keywords = KeywordsField(required=False)
    perms = forms.ChoiceField(choices=PERMS_CHOICES, widget=forms.RadioSelect(),
                              initial=NRC_FLIS)

    class Meta:

        model = Catalogue
        exclude = ('kind', 'created_by', 'created_on', 'last_updated', 'draft',
                   'perms')

        widgets = {
            'address': forms.Textarea(),
        }
        labels = {
            'status': 'Type of need',
            'need_urgent': 'Is this need urgent?',
        }

    def __init__(self, *args, **kwargs):
        self.is_draft = kwargs.pop('is_draft', False)
        request = get_current_request()
        self.user_id = request.user_id
        super(CatalogueForm, self).__init__(*args, **kwargs)

        self.fields['url'].initial = 'http://'
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

        catalogue.category = self.cleaned_data['category']
        catalogue.flis_topic = self.cleaned_data['flis_topic']
        catalogue.theme = self.cleaned_data['theme']

        catalogue.title = self.cleaned_data['title']
        catalogue.description = self.cleaned_data['description']
        catalogue.status = self.cleaned_data['status']
        catalogue.geographic_scope = self.cleaned_data['geographic_scope']
        catalogue.start_date = self.cleaned_data['start_date']
        catalogue.end_date = self.cleaned_data['end_date']
        catalogue.contact_person = self.cleaned_data['contact_person']
        catalogue.email = self.cleaned_data['email']
        catalogue.phone_number = self.cleaned_data['phone_number']
        catalogue.institution = self.cleaned_data['institution']
        catalogue.address = self.cleaned_data['address']
        catalogue.country = self.cleaned_data['country']
        catalogue.url = self.cleaned_data['url']
        catalogue.info = self.cleaned_data['info']
        catalogue.document = self.cleaned_data['document']
        catalogue.save()

        keywords = self.cleaned_data['keywords']
        catalogue.keywords.clear()
        catalogue.keywords.add(*keywords)

        perms = self.cleaned_data['perms']
        CataloguePermission.objects.get_or_create(catalogue=catalogue,
                                                  permission=perms)
        return catalogue


class NeedForm(CatalogueForm):

    KIND = 'need'

    class Meta(CatalogueForm.Meta):

        exclude = CatalogueForm.Meta.exclude + ('resources',)

        labels = {
            'status': 'Type of need',
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

    def save(self):
        catalogue = super(OfferForm, self).save()
        catalogue.resources = self.cleaned_data['resources']
        catalogue.save()
        return catalogue


class CatalogueFilterForm(forms.Form):

    KIND_CHOICES = (('all', 'All'),) + Catalogue.KIND_CHOICES

    kind = forms.ChoiceField(choices=KIND_CHOICES)


