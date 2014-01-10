
SCHEMA = 'http://projects.eionet.europa.eu/flis-services-project/' \
         'live-catalogue/static/schema.rdf'


RDF_URI = {
    'rdf_type': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
    'title': 'http://purl.org/dc/elements/1.1/title',
    'identifier': 'http://purl.org/dc/elements/1.1/identifier',
    'date': 'http://purl.org/dc/elements/1.1/date',
    'catalogue_event': SCHEMA + '#catalogue_event',
    'catalogue_kind': SCHEMA + '#catalogue_kind',
    'event_type': SCHEMA + '#event_type',
    'actor': SCHEMA + '#actor',
    'actor_name': SCHEMA + '#actor_name',
}
