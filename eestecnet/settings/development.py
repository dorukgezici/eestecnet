from basic import *
import uuid

uuid._uuid_generate_random = None

SECRET_KEY = 'o&)%bwhyl5(g)%rmq+knp%75y9s@j!a-x#3oh^rzuw$$=nld*x'

DEBUG = True
TEMPLATE_DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'eestecnet@gmail.com'
EMAIL_HOST_PASSWORD = 'eeStec4ever'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
CORS_ORIGIN_ALLOW_ALL = True
