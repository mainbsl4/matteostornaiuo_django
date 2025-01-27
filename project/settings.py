from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-m$w8san7%avlpm*x2n7ing8mri-c&wh!4wfody(30se_x2mln^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "users",
    "client",
    "staff",
    "dashboard",
    "chat",
    "shifting",
    "subscription",
    
    

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Rest framework
REST_FRAMEWORK = {
    # for auth
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
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

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILE_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# for auth
AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}



# email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "mainbsl4@gmail.com"
EMAIL_HOST_PASSWORD = "nmwk umma atdu sosv"
EMAIL_PORT = 465  # SMTP port
EMAIL_USE_SSL = True  # Use SSL for secure connection

# Stripe settings
PUBLISH_KEY = "pk_test_51MhVdoSI80DUGvJVmqHGBD9DUrbFnouO2ikPJxyWj4tpELlnViPbK2niqEgmxDvmXwjiUqNHzMXs8sfQsoW6RNM700HLRJ0ekb"
SECRET_KEY  = "sk_test_51MhVdoSI80DUGvJV2cJX44q7luc0y6updGFvyxOR5kG6blPQk2AXXg5QNNyWn7hBU8k3u6oZEDlufGbaD6ytufcJ00n6mgp4Os"
WEBHOOK_KEY = ""

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# celety configuration
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'


# UNFOLD = {

#      "SIDEBAR": {
#         "show_search": True,  # Search in applications and models names
#         "show_all_applications": True, 
#          "navigation": [
#             {
#                 "title": _("Navigation"),
#                 "separator": True,  # Top border
#                 "collapsible": True,  # Collapsible group of links
#                 "items": [
#                     {
#                         "title": _("Dashboard"),
#                         "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
#                         "link": reverse_lazy("admin:index"),
#                         # "badge": "sample_app.badge_callback",
#                         "permission": lambda request: request.user.is_superuser,
#                     },
#                     {
#                         "title": _("Users"),
#                         "icon": "people",
#                         "link": reverse_lazy("admin:users_user_changelist"),
#                     },
#                 ],
#             },
#             {
#                 "title": _("Company Profile"),
#                 "icon": "apartment",
#                 "collapsible": True, 
#                 "items":[
#                     {
#                         "title": _("Profile"),
#                         "icon": "apartment",
#                         "link": reverse_lazy("admin:client_companyprofile_changelist"),
#                     },
#                     {
#                         "title": _("Create Jobs"),
#                         "icon": "work",
#                         "link": reverse_lazy("admin:client_job_add"),
#                     }
#                 ]
#             },
            
#         ],
#     },
    

# }