import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings

    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chirps',
        'USER': 'root',
        'PASSWORD': 'chirp47',
        'HOST': '',
        'PORT': ''
    }

    settings.CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
