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
        "Add a simple validator that just validates an item meets a format."
        if message_key is None:
            message_key = name
        error_message = self.field.error_messages.get(message_key)
        self._validators[name] = {'error_message': error_message}

    def add_param_validator(self, name, message_key=None):
        "Add a validator that takes a single param"
        if message_key is None:
            message_key = name
        value = getattr(self.field, name, None)
        if value:
            error_message = self.field.error_messages.get(message_key)
            self._validators[name] = {'value': value, 'error_message': error_message}

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

# These fields require nothing specialised they will be assigned AjaxField by
# default in the factory method:
#   BooleanField, ChoiceField, TypedChoiceField, MultipleChoiceField
#
# File fields have limited capability for validation on the client side and will
# be treated the same as the above fields, these include:
#   FileField, FilePathField, ImageField

# Text fields

class AjaxCharField(AjaxField):
    def parse(self):
        super(AjaxCharField, self).parse()
        self.add_param_validator('max_length')
        self.add_param_validator('min_length')
register(forms.CharField, AjaxCharField)

class AjaxEmailField(AjaxCharField):
    def parse(self):
        super(AjaxEmailField, self).parse()
        self.add_simple_validator('is_email', message_key='invalid')
register(forms.EmailField, AjaxEmailField)

class AjaxRegexField(AjaxCharField):
     def parse(self):
        super(AjaxRegexField, self).parse()
        # TODO: Pass defined regex to client
register(forms.RegexField, AjaxRegexField)

class AjaxURLField(AjaxCharField):
     def parse(self):
        super(AjaxURLField, self).parse()
        self.add_simple_validator('is_url', message_key='invalid')
register(forms.URLField, AjaxURLField)


# Numberic fields

class AjaxNumericField(AjaxField):
    def parse(self):
        super(AjaxNumericField, self).parse()
        self.add_param_validator('max_value')
        self.add_param_validator('min_value')

class AjaxFloatField(AjaxNumericField):
    def parse(self):
        super(AjaxFloatField, self).parse()
        self.add_simple_validator('is_float', message_key='invalid')
register(forms.FloatField, AjaxFloatField)

class AjaxDecimalField(AjaxFloatField):
    def parse(self):
        super(AjaxDecimalField, self).parse()
        self.add_param_validator('max_digits')
        self.add_param_validator('decimal_places')
register(forms.DecimalField, AjaxDecimalField)

class AjaxIntegerField(AjaxNumericField):
    def parse(self):
        super(AjaxIntegerField, self).parse()
        self.add_simple_validator('is_int', message_key='invalid')
register(forms.IntegerField, AjaxIntegerField)


# Date time fields

class AjaxDateField(AjaxField):
    def parse(self):
        super(AjaxDateField, self).parse()
        # Todo: Parse input_formats
register(forms.DateField, AjaxDateField)

class AjaxDateTimeField(AjaxField):
    def parse(self):
        super(AjaxDateTimeField, self).parse()
        # Todo: Parse input_formats
register(forms.DateTimeField, AjaxDateTimeField)

class AjaxTimeField(AjaxField):
    def parse(self):
        super(AjaxTimeField, self).parse()
        # Todo: Parse input_formats
register(forms.TimeField, AjaxTimeField)


# Special cases

class AjaxIPAddressField(AjaxField):
    def parse(self):
        super(AjaxIPAddressField, self).parse()
        self.add_simple_validator('is_ipaddress', message_key='invalid')
register(forms.IPAddressField, AjaxIPAddressField)

class AjaxNullBooleanField(AjaxField):
    def parse(self):
        # Required is NEVER checked for this field so prevent it being added
        pass
register(forms.NullBooleanField, AjaxNullBooleanField)
