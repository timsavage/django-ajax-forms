# Copyright 2009 Tim Savage <tim.savage@poweredbypenguins.org>
# Licensed under the terms of the BSD License (see LICENSE)
from django.template.defaulttags import register
from ajax_forms.utils import form_to_json

@register.simple_tag
def render_ajax_fields(form):
    """
    This will render a Django form into an ajax.

    Usage::

        {% render_ajax_form form %}

    """
    return form_to_json(form)

@register.simple_tag
def as_dl(form, errors_on_separate_row=True):
    """
    Render form as a dl construct

    Usage::

        {% as_dl form %}

    """
    return form._html_output(
        u'<dt>%(label)s</dt><dd>%(field)s%(help_text)s%(errors)s</dd>', 
        u'<li>%s</li>', 
        '</dd>', 
        u' %s', 
        errors_on_separate_row)
