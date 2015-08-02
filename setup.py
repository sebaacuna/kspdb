#!/usr/bin/env python
from setuptools import setup, find_packages

project_name = "kspdb"

setup(name=project_name,
      version='0.1',
      packages=find_packages(),
      package_data={project_name: ['static/*.*', 'templates/*.*']},
      scripts=[ "manage.py"]
)