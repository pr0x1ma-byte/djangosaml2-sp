"""
Django settings for poc project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pc4=clnq=5y*0bd&nu**&fe1m3v+5&v3nkuhlr()9z%gig))_*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosaml2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
]

ROOT_URLCONF = 'poc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'poc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# ******

LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SAMESITE=None

import saml2
from os import path
import saml2.saml

SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_POST


BASEDIR = path.dirname(path.abspath(__file__))
SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    'xmlsec_binary': '/usr/bin/xmlsec1',

    # your entity id, usually your subdomain plus the url to the metadata view
    'entityid': 'python:saml2:test:1',

    # directory with attribute mapping
    # // look at this...
    'attribute_map_dir': path.join(BASE_DIR, 'attributemaps'),

    # this block states what services we provide
    'service': {
        # we are just a lonely SP
        'sp' : {
            'authn_requests_signed':True,
            'want_response_signed':False,

            'name': 'python:saml2:test:1',
            'name_id_format': saml2.saml.NAMEID_FORMAT_PERSISTENT,
            'endpoints': {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                'assertion_consumer_service': [
                    ('http://localhost:80/saml2/acs/',
                     saml2.BINDING_HTTP_POST),
                ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                'single_logout_service': [
                    ('http://localhost:80/saml2/ls/',
                     saml2.BINDING_HTTP_REDIRECT),
                    ('http://localhost:80/saml2/ls/post/',
                     saml2.BINDING_HTTP_POST),
                ],
            },

            # attributes that this project need to identify a user
            'required_attributes': ['uid'],

            # attributes that may be useful to have but not required
            'optional_attributes': ['eduPersonAffiliation'],

            # in this section the list of IdPs we talk to are defined
            'idp': {
                # we do not need a WAYF service since there is
                # only an IdP defined here. This IdP should be
                # present in our metadata

                # the keys of this dictionary are entity ids
                'https://samltest.id/saml/idp': {
                    'single_sign_on_service': {
                        saml2.BINDING_HTTP_REDIRECT: '"https://samltest.id/idp/profile/SAML2/Redirect/SSO',
                    },
                    'single_logout_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://samltest.id/idp/profile/SAML2/Redirect/SLO',
                    },
                },
            },
        },
    },

    # where the remote metadata is stored
    'metadata': {
        #'local': [path.join(BASE_DIR, 'python-sp.xml')]
        'local': [path.join(BASE_DIR, 'idp.xml'),path.join(BASE_DIR, 'python-sp.xml')]
      #  'remote': path.join(BASE_DIR, 'idp.xml'),
    },

    # set to 1 to output debugging information
    'debug': 1,

    # Signing
    'key_file': path.join(BASE_DIR, 'private.pem'),  # private part
    'cert_file': path.join(BASE_DIR, 'public.pem'),  # public part

    # Encryption
    'encryption_keypairs': [{
        'key_file': path.join(BASE_DIR, 'private.pem'),  # private part
        'cert_file': path.join(BASE_DIR, 'public.pem'),  # public part
    }],

    # own metadata settings
    'contact_person': [
        {'given_name': 'Lorenzo',
         'sur_name': 'Gil',
         'company': 'Yaco Sistemas',
         'email_address': 'lgs@yaco.es',
         'contact_type': 'technical'},
        {'given_name': 'Angel',
         'sur_name': 'Fernandez',
         'company': 'Yaco Sistemas',
         'email_address': 'angel@yaco.es',
         'contact_type': 'administrative'},
    ],
    # you can set multilanguage information here
    'organization': {
        'name': [('Yaco Sistemas', 'es'), ('Yaco Systems', 'en')],
        'display_name': [('Yaco', 'es'), ('Yaco', 'en')],
        'url': [('http://www.yaco.es', 'es'), ('http://www.yaco.com', 'en')],
    },
    'valid_for': 24,  # how long is our metadata valid
}