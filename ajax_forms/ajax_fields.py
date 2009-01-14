from django import forms
from django.utils.translation import ugettext as _

class AlreadyRegistered(Exception):
    "An attempt was made to register a form field more than once"
    pass

registry = {}

def register(field, ajax_field):
    "Register an ajax_field for a field"
    if field in registry:
        raise AlreadyRegistered(_('The form field %s has already been registered.') % field.__name__)
    registry[field] = ajax_field

def factory(field_instance):
    "Get a ajax_field instance for a feild instance"
    ajax_field = registry.get(type(field_instance), AjaxField)
    return ajax_field(field_instance)

class AjaxField(object):
    "Base field mask"
    def __init__(self, field):
        self.field = field
        self._validators = None

    def add_simple_validator(self, name, message_key=None):
        "Add a simple validator that has a value and a message"
        if message_key is None:
            message_key = name
        param = getattr(self.field, name, None)
        if param:
            message = self.field.error_messages.get(message_key)
            self._validators[name] = {'param': param, 'message': message}

    def parse(self):
        "Hook for doing any extra parsing in sub class"
        if self.field.required:
            self.add_simple_validator('required')

    def _get_validators(self):
        if self._validators is None:
            self._validators = {}
            self.parse()
        return self._validators
    validators = property(_get_validators)


class AjaxCharField(AjaxField):
    def parse(self):
        super(AjaxCharField, self).parse()
        self.add_simple_validator('max_length')
        self.add_simple_validator('min_length')

register(forms.CharField, AjaxCharField)
register(forms.RegexField, AjaxCharField)
