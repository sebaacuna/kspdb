# Import global settings to make it easier to extend settings.
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from .paths import PROJECT_DIR, PROJECT_NAME, VAR_ROOT
import os
import milieu

M = milieu.init()

# ==============================================================================
# Generic Django project settings
# ==============================================================================
DEBUG = M.DEBUG or False
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'GMT'
USE_I18N = True
SITE_ID = 1

SECRET_KEY = M.SECRET_KEY

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

ADMINS = (
    ('Administrator', M.ADMIN_EMAIL or "admin@unholster.com"),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = (M.ALLOWED_HOSTS,)

# ==============================================================================
# Project URLS and media settings
# ==============================================================================

ROOT_URLCONF = PROJECT_NAME + '.conf.urls'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'


# =============================================================================
# Static files and frontend
# =============================================================================
FRONT_BUILD_DIR = 'static'
STATIC_DOMAIN = M.STATIC_DOMAIN
STATIC_URL = M.STATIC_URL or ('/static/%s/' % PROJECT_NAME)
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, PROJECT_NAME, FRONT_BUILD_DIR),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = M.MEDIA_URL or ('/uploads/%s/' % PROJECT_NAME)
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')


# ==============================================================================
# Middlewares
# ==============================================================================
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# ==============================================================================
# Templates
# ==============================================================================
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, PROJECT_NAME, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    # 'Custom context processors here',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

# =============================================================================
# Databases
# =============================================================================
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=M.DATABASE_URL)}

# =============================================================================
# Caching
# =============================================================================
if M.MEMCACHE_SERVERS:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': M.MEMCACHE_SERVERS,
            'TIMEOUT': 0,
            'BINARY': True,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

CACHES['staticfiles'] = {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'staticfiles'
}

# =============================================================================
# Apps
# =============================================================================
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'password_reset',
    'bootstrapform',
    'frontflow',
    'social.apps.django_app.default',
    'kspdb.apps.main',
)

# =============================================================================
# Logging
# =============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'  # noqa
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'requests': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        PROJECT_NAME: {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}


# =============================================================================
# Github signin
# =============================================================================
AUTHENTICATION_BACKENDS = (
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

SOCIAL_AUTH_GITHUB_KEY = '1a1282b1616b3ab1a469'
SOCIAL_AUTH_GITHUB_SECRET = '924731c603a4a6ae71bf192666eb7ac60475900a'
SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details',

    'kspdb.apps.main.pipeline.save_data',
)
