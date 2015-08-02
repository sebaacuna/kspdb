#!/usr/bin/env python
import os
import sys

PROJECT_NAME = "kspdb"
TESTING = "test" in sys.argv or "test_coverage" in sys.argv
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'dev')

if TESTING:
    DJANGO_ENV = 'test'

settings_module = '%s.conf.%s_settings' % (PROJECT_NAME, DJANGO_ENV)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
