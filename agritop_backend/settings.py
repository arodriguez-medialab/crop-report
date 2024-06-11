import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i)nf44xsxv)yr(=!i4*8f@_n(ank0i-durbs5b!4(%&^$@29qw'

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('DEBUG_MODE') == "False":
    DEBUG = False
    ALLOWED_HOSTS = [os.getenv('BACKEND_URL').split("//")[1]]
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split()
else:
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True
    env = environ.Env()
    environ.Env.read_env()


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'authentication',
    'file_manager',
    'plantation',
    'user',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'storages',
    'background_task',
]

INSTALLED_APPS = INSTALLED_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'authentication.auth_backend.CustomAuthBackend', 'django.contrib.auth.backends.ModelBackend'
]

AUTH_USER_MODEL = 'user.User'


ROOT_URLCONF = 'agritop_backend.urls'
TEMPLATE_DIR = os.path.join(ROOT_DIR, "agritop_backend/templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'agritop_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
if os.getenv('DEBUG_MODE') == "False":
    DEFAULT_FILE_STORAGE = 'azure_storage.custom_azure.AzureMediaStorage'
    #STATICFILES_STORAGE = 'azure_storage.custom_azure.AzureStaticStorage'
    #STATIC_LOCATION = "static"
    STATIC_URL = '/static/'
    MEDIA_LOCATION = "media"
    AZURE_ACCOUNT_NAME = os.getenv('AZURE_BLOB_STORAGE_ACCOUNT_NAME')
    AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
    #STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
    STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')
    STATICFILES_DIRS = (os.path.join(ROOT_DIR, 'agritop_backend/static'),)
else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')
    STATICFILES_DIRS = (os.path.join(ROOT_DIR, 'agritop_backend/static'),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MAX_ATTEMPTS = 1


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Crop-Report Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Crop-Report Admin",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Crop-Report",

    # Welcome text on the login screen
    "welcome_sign": "Bienvenido a Crop-Report Admin",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

     # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "images/agritop_logo_100_50.jpg",

    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": 'styles/style_custom.css',


    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "user.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "background_task.completedtask": "fas fa-list",
        "background_task.task": "fas fa-bars",
        "plantation.client": "fas fa-seedling",
        "plantation.crop": "fas fa-seedling",
        "plantation.plantationdivision": "fas fa-seedling",
        "plantation.plantation": "fas fa-seedling",
        "plantation.land": "fas fa-image",
        "plantation.ndvi": "fas fa-signal",
        "plantation.cropvariety": "fas fa-seedling",
        "plantation.landinfo": "fas fa-file-word",
        "plantation.plantationdivisionvariety": "fas fa-seedling",
        "plantation.location": "fas fa-map"
    },

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    #"related_modal_active": True,

    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "order_with_respect_to": ["plantation", "background_task", "user"],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
}

if os.getenv('DEBUG_MODE') == "False":
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_TRUSTED_ORIGINS = ['https://portal-agritop-backend.azurewebsites.net']

LOGOUT_REDIRECT_URL = '/admin'

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"