import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# for test only to get the user details. frame.requests.get is mocked
FRAME_URL = True


SKIP_EDIT_AUTHORIZATION = False


# disable frame.Loader in tests, don't need it
TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader',)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_ROOT = os.path.join(BASE_DIR, 'live_catalogue', 'static')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

FROM_EMAIL = 'no-reply@eaudeweb.ro'
