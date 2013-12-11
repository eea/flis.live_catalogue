import factory
from live_catalogue import models


class CategoryFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Category
    FACTORY_DJANGO_GET_OR_CREATE = ('handle', 'title',)

    handle = 'projects'
    title = 'Projects'


class FlisTopicFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.FlisTopic
    FACTORY_DJANGO_GET_OR_CREATE = ('handle', 'title',)

    handle = 'early-warning'
    title = 'Early warning'


class ThemeFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Theme
    FACTORY_DJANGO_GET_OR_CREATE = ('handle', 'title',)

    handle = 'air-pollution'
    title = 'Air pollution'


class CatalogueFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Catalogue

    categories = factory.SubFactory(CategoryFactory)
    flis_topics = factory.SubFactory(FlisTopicFactory)

    subject = 'Catalogue'
    description = 'Catalogue description'

    contact_person = 'John Doe'
    email = 'john.doe@eaueweb.ro'
    url = 'http://john.doe.eaudeweb.ro'
    institution = 'EEA'
    country = 'at'


class NeedFactory(CatalogueFactory):

    kind = models.Catalogue.NEED


class OfferFactory(CatalogueFactory):

    kind = models.Catalogue.OFFER
