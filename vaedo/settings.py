import os
import environ
from pathlib import Path

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')


ALLOWED_HOSTS = ['192.168.10.18', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",


    "corsheaders", # for request diferent origin
    "modeltranslation",
    'django.contrib.admin',  # optional
    'django.contrib.postgres',
    'django.contrib.gis',
    "rest_framework",
    # "rest_framework_gis",

    'main',
    'futur',


]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.locale.LocaleMiddleware",  ##lenguage
    "corsheaders.middleware.CorsMiddleware", ## for request diferent origin
    
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "vaedo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "vaedo.wsgi.application"


DATABASES = {
     'default': {
         "ENGINE": "django.contrib.gis.db.backends.postgis",
         'HOST': env('DB_HOST'),
         'NAME': env('DB_NAME'),
         'USER': env('DB_USER'),
         'PASSWORD': env('DB_PASS')
     }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ("en", gettext("English")),
    ("ru", gettext("Russia")),
    ("hy", gettext("Armenian")),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("en", "ru", "hy")



STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

REST_FRAMEWORK = { 
    'DEFAULT_PERMISSION_CLASSES' : [ 
        'rest_framework.permissions.AllowAny' , 
    ] 
} 
