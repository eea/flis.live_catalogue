from django.db import models
from live_catalogue.definitions import CATEGORIES, FLIS_TOPICS, THEMES
from live_catalogue.definitions import GEOGRAPHIC_SCOPE, COUNTRIES


class Catalogue(models.Model):

    OFFER = 'offer'
    NEED = 'need'
    KIND_CHOICES = (
        (NEED, 'Need'),
        (OFFER, 'Offer'),
    )

    OFFICIAL = 'official'
    INFORMAL = 'informal'
    STATUS_CHOICES = (
        (OFFICIAL, 'Official'),
        (INFORMAL, 'Informal'),
    )

    kind = models.CharField(choices=KIND_CHOICES, max_length=5, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    draft = models.BooleanField(default=True)
    user_id = models.CharField(max_length=64, blank=True)

    category = models.CharField(choices=CATEGORIES, max_length=64)
    flis_topic = models.CharField(choices=FLIS_TOPICS, max_length=64)
    theme = models.CharField(choices=THEMES, max_length=64)

    title = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    keywords = models.ManyToManyField('Keyword', null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, blank=True)
    geographic_scope = models.CharField(choices=GEOGRAPHIC_SCOPE, max_length=128,
                                        blank=True)
    resources = models.TextField(blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    need_urgent = models.BooleanField(default=False)

    contact_person = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    phone_number = models.CharField(max_length=64, blank=True)
    institution = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=256, blank=True)
    country = models.CharField(choices=COUNTRIES, max_length=64, blank=True)
    url = models.URLField(blank=True)
    info = models.TextField(blank=True)
    document = models.FileField(upload_to='documents', null=True, blank=True)

    def __unicode__(self):
        return '%s (%s)' % (self.kind, self.title)

    @property
    def kind_verbose(self):
        return dict(self.KIND_CHOICES).get(self.kind, '')

    @property
    def category_verbose(self):
        return dict(CATEGORIES).get(self.category, '')

    @property
    def flis_topic_verbose(self):
        return dict(FLIS_TOPICS).get(self.flis_topic, '')

    @property
    def theme_verbose(self):
        return dict(THEMES).get(self.theme, '')

    @property
    def status_verbose(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')

    @property
    def geographic_scope_verbose(self):
        return dict(GEOGRAPHIC_SCOPE).get(self.geographic_scope, '')

class CataloguePermission(models.Model):

    catalogue = models.ForeignKey(Catalogue, related_name='permissions')
    permission = models.CharField(max_length=64)


class Keyword(models.Model):

    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name
