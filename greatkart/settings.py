import os
from pathlib import Path
from decouple import config, UndefinedValueError
import sys

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# -----------------------
# GÜVENLİ DEĞİŞKEN OKUMA FONKSİYONU
# -----------------------
def get_config(key, default=None, cast=str):
    try:
        return config(key, default=default, cast=cast)
    except Exception as e:
        print(f"HATA: {key} okunamadı. Detay: {e}", file=sys.stderr)
        return default

# Loglarda durumu görmek için
print(f"--- UYGULAMA BAŞLATIILIYOR ---", file=sys.stderr)
print(f"DEBUG DURUMU: {get_config('DEBUG', default='True')}", file=sys.stderr)

# -----------------------
# SECURITY
# -----------------------
SECRET_KEY = get_config('SECRET_KEY', default='django-insecure-test-key-12345')
DEBUG = get_config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = get_config(
    'ALLOWED_HOSTS',
    default='127.0.0.1,localhost,greatkart-django-3dhm.onrender.com,devturks.com,www.devturks.com',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

CSRF_TRUSTED_ORIGINS = get_config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://greatkart-django-3dhm.onrender.com,https://devturks.com,https://www.devturks.com',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

# -----------------------
# INSTALLED APPS
# -----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'accounts',
    'store',
    'carts',
    'orders',
    'storages',
]

# -----------------------
# MIDDLEWARE
# -----------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'greatkart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'greatkart.wsgi.application'
AUTH_USER_MODEL = 'accounts.Account'

# -----------------------
# DATABASE (NEON DB)
# -----------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': get_config('DB_NAME', default='neondb'),
#         'USER': get_config('DB_USER', default='neondb_owner'),
#         'PASSWORD': get_config('DB_PASSWORD', default=''),
#         'HOST': get_config('DB_HOST', default=''),
#         'PORT': get_config('DB_PORT', default=5432, cast=int),
#         'OPTIONS': {'sslmode': 'require'},
#     }
# }
# settings.py içindeki DATABASES kısmını tamamen sil ve bunu yapıştır
# settings.py içindeki veritabanı bölümünü bununla değiştir abi
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_mniq6JDNf7YH',
        'HOST': 'ep-wild-bird-agyp5w1u-pooler.c-2.eu-central-1.aws.neon.tech',
        'PORT': 5432,
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}
# -----------------------
# STATIC & MEDIA (AWS S3)
# -----------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

AWS_ACCESS_KEY_ID = get_config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = get_config('AWS_S3_REGION_NAME', default='eu-north-1')

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------
# EMAIL SETTINGS
# -----------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = get_config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_config('EMAIL_HOST_PASSWORD')

# -----------------------
# OTHER SETTINGS
# -----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 86400
SESSION_EXPIRE_AT_BROWSER_CLOSE = False