#!/usr/bin/env python
from setuptools import setup, find_packages
from os.path import join, dirname
import ajax_forms

if 'final' in ajax_forms.VERSION[-1]:
    CLASSIFIERS = ['Development Status :: 5 - Stable']
elif 'beta' in ajax_forms.VERSION[-1]:
    CLASSIFIERS = ['Development Status :: 4 - Beta']
else:
    CLASSIFIERS = ['Development Status :: 3 - Alpha']
CLASSIFIERS += [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name="django-ajax-forms",
    version=ajax_forms.__version__,
    url="http://code.google.com/p/django-ajax-forms/",
    author="Tim Savage",
    author_email="tim.savage@poweredbypenguins.org",
    license="BSD License",
    description="Client side JavaScript validation for any Django form.",
    long_description=open(join(dirname(__file__), 'README')).read(),
    classifiers=CLASSIFIERS,
    platforms=['OS Independent'],
    packages=find_packages(exclude=["example", "example.*"]),
    package_data = {'ajax_forms': ['static/js/*.js']},
    zip_safe = False,
)
