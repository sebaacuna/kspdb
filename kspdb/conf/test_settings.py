from .settings import *  # NOQA

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# =============================================================================
# Testing
# =============================================================================
del STATICFILES_STORAGE
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# This hasher makes tests run faster
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Don't test external modules that are maintained as a separate effort
COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'common.views.test', '__init__', 'django',
    'gunicorn', 'djsupervisor', 'migrations',
    'south.', 'test_', 'admin$',
    'debug_toolbar'
]

COVERAGE_REPORT_HTML_OUTPUT_DIR = "/tmp/coverage"
