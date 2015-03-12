#!/usr/bin/env python

import setuplib
from pip.req import parse_requirements
from codecs import open  # To use a consistent encoding
from os import path
import sys
import os

import horizon_contrib

PACKAGE_NAME = 'horizon-contrib'
PACKAGE_DIR = 'horizon_contrib'
extra = {}

here = path.abspath(path.dirname(__file__))
packages, package_data = setuplib.find_packages('horizon_contrib')

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()
with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as f:
    history = f.read()
with open(path.join(here, 'LICENSE'), encoding='utf-8') as f:
    license = f.read()

setup(
    name=PACKAGE_NAME,
    version=__import__('contrib').__version__,
    description='Horizon Django tools.',
    author='Michael Kuty, Ales Komarek',
    author_email='mail@majklk.cz, mail@newt.cz',
    url='https://github.com/michaelkuty/horizon-contrib.git',
    license=license,
    long_description=readme + '\n\n' + history,
    platforms=['any'],
    packages=packages,
    package_data=package_data,
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django, Horizon',
        'Intended Audikedbe :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)