# Copyright 2009 Tim Savage <tim.savage@jooceylabs.com>
# See LICENSE for licence information

from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.forms import Form
from django.utils.datastructures import SortedDict
from django.utils.encoding import force_unicode
from django.utils.functional import Promise
from django.utils.translation import ugettext as _

from ajax_forms.ajax_fields import factory as field_factory


class LazyEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

json_serializer = LazyEncoder()


def form_to_json(form):
    if not isinstance(form, Form):
        raise TypeError(_("Expected Django Form"))
    ajax_directives = getattr(form, 'Ajax', None)

    # Generate ajax fields
    exclude_fields = getattr(ajax_directives, 'exclude_fields', [])
    ajax_fields = SortedDict()
    for name, field in form.fields.items():
        if name in exclude_fields:
            continue
        # If field supplies it's own info use that
        if hasattr(field, 'to_ajax'):
            ajax_fields[name] = field.to_ajax()
        else:
            ajax_field = field_factory(field)
            ajax_fields[name] = ajax_field.to_ajax()

    # Add ajax callbacks
    #~ callback_url = getattr(ajax_directives, 'callback_url', '')
    #~ for callback_field in getattr(ajax_directives, 'callback_fields', []):
        #~ try:
            #~ ajax_fields[callback_field]['callback'] = callback_url
        #~ except KeyError:
            #~ raise Exception(_('Field "%s" not found in this form') % name)

    # Add additional rules
    for name, rules in getattr(ajax_directives, 'rules', []):
        try:
            ajax_fields[name].setdefault('rules', {}).update(rules)
        except KeyError:
            raise Exception(_('Field "%s" not found in this form') % name)

    # Add additional messages
    for name, messages in getattr(ajax_directives, 'messages', []):
        try:
            ajax_fields[name].setdefault('msgs', {}).update(messages)
        except KeyError:
            raise Exception(_('Field "%s" not found in this form') % name)

    return json_serializer.encode(ajax_fields)
