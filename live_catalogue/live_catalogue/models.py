from django.db import models
from live_catalogue.definitions import COUNTRIES
from notifications.utils import get_user_name


class Category(models.Model):

    handle = models.SlugField(primary_key=True)
    title = models.CharField(max_length=64)

    def __unicode__(self):
        return self.title


class FlisTopic(models.Model):

    handle = models.SlugField(primary_key=True)
    title = models.CharField(max_length=64)

    def __unicode__(self):
        return self.title


class Theme(models.Model):

    handle = models.SlugField(primary_key=True)
    title = models.CharField(max_length=64)

    def __unicode__(self):
        return self.title


class Document(models.Model):

    name = models.FileField(upload_to='documents')

    def __unicode__(self):
        return self.name.name


class Catalogue(models.Model):

    OFFER = 'offer'
    NEED = 'need'
    KIND_CHOICES = (
        (NEED, 'Need'),
        (OFFER, 'Offer'),
    )

    OFFICIAL = 'official'
    INFORMAL = 'informal'
    TYPE_OF_CHOICES = (
        (OFFICIAL, 'Official'),
        (INFORMAL, 'Informal'),
    )

    OPEN = 'open'
    SOLVED = 'solved'
    CLOSED = 'closed-without-solution'
    DRAFT = 'draft'
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (SOLVED, 'Solved'),
        (CLOSED, 'Closed without solution'),
        (DRAFT, 'Draft'),
    )

    kind = models.CharField(choices=KIND_CHOICES, max_length=5, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    draft = models.BooleanField(default=True)
    user_id = models.CharField(max_length=64, blank=True)

    categories = models.ManyToManyField(Category)
    flis_topics = models.ManyToManyField(FlisTopic)
    themes = models.ManyToManyField(Theme, blank=True, verbose_name='Topics')

    subject = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=32,
                              blank=True, default=OPEN)
    type_of = models.CharField(choices=TYPE_OF_CHOICES, max_length=10,
                               blank=True)
    resources = models.TextField(blank=True)

    need_urgent = models.BooleanField(default=False)

    contact_person = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    phone_number = models.CharField(max_length=64, blank=True)
    institution = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=256, blank=True)
    country = models.CharField(choices=COUNTRIES, max_length=64, blank=True)
    url = models.URLField(blank=True)
    info = models.TextField(blank=True,
                            verbose_name='Additional contact details')
    documents = models.ManyToManyField(Document, null=True, blank=True)

    def __unicode__(self):
        return '%s (%s)' % (self.kind, self.subject)

    @property
    def kind_verbose(self):
        return dict(self.KIND_CHOICES).get(self.kind, '')

    @property
    def type_of_verbose(self):
        return dict(self.TYPE_OF_CHOICES).get(self.type_of, '')

    @property
    def status_verbose(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')

    @property
    def country_verbose(self):
        return dict(COUNTRIES).get(self.country, '')

    @property
    def user_full_name(self):
        return get_user_name(self.user_id)
