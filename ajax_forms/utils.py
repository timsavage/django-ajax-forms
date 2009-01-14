from simplejson import JSONEncoder

from django.utils.functional import Promise
from django.utils.encoding import force_unicode

from ajax_forms.ajax_fields import factory as field_factory

__all__ = (
    'form_to_json'
)

class LazyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

json_serializer = LazyEncoder()


def form_to_json(form):
    data = []
    for name, field in form.fields.items():
        ajax_field = field_factory(field)
        data.append({'name': form.add_prefix(name), 'validators': ajax_field.validators})
    return json_serializer.encode(data)
