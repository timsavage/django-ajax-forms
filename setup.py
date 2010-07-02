#!/usr/bin/env python
from distutils.core import setup

setup(
    name = "django-ajax-forms",
    version = open('VERSION').read().strip(),
    url = "http://code.google.com/p/django-ajax-forms/",
    author = "Tim Savage",
    author_email = "tim.savage@jooceylabs.com",
    license = "BSD License",
    description = "Client side JavaScript validation for any Django form.",
    long_description = open('README').read(),
    platforms=['OS Independent'],
    packages = ['ajax_forms', 'ajax_forms.templatetags'],
    package_data = {'ajax_forms': ['media/js/*.js']},
    zip_safe = False,
)
