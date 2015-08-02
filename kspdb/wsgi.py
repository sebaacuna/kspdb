import os
import sys
import site
from conf.paths import PROJECT_DIR

site.addsitedir('%s/lib/python%d.%d/site-packages' % (
    PROJECT_DIR, sys.version_info[0], sys.version_info[1])
)
sys.stdout = sys.stderr


PROJECT_NAME = "kspdb"
TESTING = "test" in sys.argv or "test_coverage" in sys.argv
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'dev')

if TESTING:
    DJANGO_ENV = 'test'

settings_module = '%s.conf.%s_settings' % (PROJECT_NAME, DJANGO_ENV)

os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
