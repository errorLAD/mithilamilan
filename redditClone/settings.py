import os
from pathlib import Path
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if available
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')

ALLOWED_HOSTS = [
    "*",
    "mithilamilan.in",
    "www.mithilamilan.in",
    "web-production-76926.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://web-production-76926.up.railway.app",
    "https://mithilamilan.in",
]

# Application definition
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'users',
    'posts',
    'subreddits',
    'pg_rental',
    'delhi_wiki',
    'bus_service',
    'coupon_service',
    'static_pages',
    'metro',
    'medical.apps.MedicalConfig',
    'hotel_service.apps.HotelServiceConfig',
    'job_portal',
    'lost_and_found',
    'storytelling',
    'news',
    'notifications',
    'events',
    'pandits',
    'mithila_pride',
    'store',
    'cab_auto',
    'ghatkaiti',
    'mithila_panchang',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'redditClone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.location_and_nav_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'redditClone.wsgi.application'

import socket

def is_host_resolvable(host, port=5432):
    if not host:
        return False
    try:
        socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        return True
    except Exception:
        return False

# Database
DATABASE_URL = os.environ.get('DATABASE_URL')
USE_LOCAL_DB = os.environ.get('USE_LOCAL_DB', 'False').lower() in ('true', '1', 't')

db_host_ok = False
if DATABASE_URL:
    try:
        parsed_temp = urlparse(DATABASE_URL)
        db_host_ok = is_host_resolvable(parsed_temp.hostname, parsed_temp.port or 5432)
    except Exception:
        db_host_ok = False

if DATABASE_URL and db_host_ok and not USE_LOCAL_DB:
    if dj_database_url:
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
            )
        }
    else:
        parsed_db = urlparse(DATABASE_URL)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': parsed_db.path.lstrip('/'),
                'USER': unquote(parsed_db.username) if parsed_db.username else '',
                'PASSWORD': unquote(parsed_db.password) if parsed_db.password else '',
                'HOST': parsed_db.hostname or '',
                'PORT': str(parsed_db.port) if parsed_db.port else '5432',
                'CONN_MAX_AGE': 600,
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Authentication settings
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/' 