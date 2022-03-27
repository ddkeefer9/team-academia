from django.conf import settings
import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dthktrmhukj7v',  
        'USER': 'smjpagjweyjiik', 
        'PASSWORD' : 'c8a599448a398d1ab2f9d7b1896cb0cb4d72404c291797e00c48f35f26a3e69d', 
        #'HOST' : '18.221.82.10',
        'HOST' : 'ec2-3-225-213-67.compute-1.amazonaws.com',
        'PORT' : '5432',
    }