from django import forms
from django.utils.translation import ugettext as _


class AlreadyRegistered(Exception):
    "An attempt was made to register a form field more than once"
    pass


registry = {}


def register(field, ajax_field):
    "Register an ajax_field for a field"
    if field in registry:
        raise AlreadyRegistered(
            _('The form field %s has already been registered.') %
                field.__name__)
    registry[field] = ajax_field


def factory(field_instance, name):
    "Get a ajax_field instance for a feild instance"
    ajax_field = registry.get(type(field_instance), AjaxField)
    return ajax_field(field_instance, name)


class AjaxField(object):
    "Base field mask"

    data_type = "String"

    def __init__(self, field_instance, name):
        self.field = field_instance
        self.name = name
        self._rules = None
        self._error_messages = {}

    def add_error_message(self, message_key):
        "Add an error message to be sent to client"
        self._error_messages[message_key] = \
            self.field.error_messages.get(message_key)

    def add_simple_rule(self, name, message_key=None):
        "Add a simple validator that just validates an item meets a format."
        if message_key is None:
            message_key = name
        self.add_error_message(message_key)
        self._rules[name] = None

    def add_param_rule(self, name, value=None, message_key=None):
        "Add a validator that takes a single param"
        if message_key is None:
            message_key = name
        if value is None:
            value = getattr(self.field, name, None)
        if value:
            self.add_error_message(message_key)
            self._rules[name] = value

    def parse(self):
        "Hook for doing any extra parsing in sub class"
        pass

    def to_ajax(self):
        if self._rules is None:
            self._rules = {}
            if self.field.required:
                self._error_messages['required'] = \
                    self.field.error_messages.get('required')
            self.parse()
        return {
            'name': self.name,
            'type': self.data_type,
            'msgs': self._error_messages,
            'rules': self._rules,
            'required': self.field.required,
        }


# These fields require nothing specialised they will be assigned AjaxField by
# default in the factory method:
#   BooleanField, NullBooleanField, ChoiceField, MultipleChoiceField,
#   TypedChoiceField
#
# File fields have limited capability for validation on the client side and
# will be treated the same as the above fields, these include:
#   FileField, FilePathField, ImageField


class AjaxCharField(AjaxField):

    data_type = 'string'

    def parse(self):
        super(AjaxCharField, self).parse()
        self.add_param_rule('max_length')
        self.add_param_rule('min_length')

register(forms.CharField, AjaxCharField)


class AjaxRegexField(AjaxCharField):

    def parse(self):
        super(AjaxRegexField, self).parse()
        self.add_param_rule('regex', self.field.regex.pattern, 'invalid')

register(forms.RegexField, AjaxRegexField)
register(forms.URLField, AjaxRegexField)
register(forms.IPAddressField, AjaxRegexField)


class AjaxEmailField(AjaxCharField):

    def parse(self):
        super(AjaxEmailField, self).parse()
        self.add_simple_rule('email', 'invalid')

register(forms.EmailField, AjaxEmailField)


class AjaxNumericField(AjaxField):

    data_type = 'number'

    def parse(self):
        super(AjaxNumericField, self).parse()
        self.add_error_message('invalid')
        self.add_param_rule('max_value')
        self.add_param_rule('min_value')

register(forms.FloatField, AjaxNumericField)


class AjaxDecimalField(AjaxNumericField):

    def parse(self):
        super(AjaxDecimalField, self).parse()
        self.add_param_rule('max_digits')
        self.add_param_rule('decimal_places')

register(forms.DecimalField, AjaxDecimalField)


class AjaxIntegerField(AjaxNumericField):

    data_type = 'int'

register(forms.IntegerField, AjaxIntegerField)


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
