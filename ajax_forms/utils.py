from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_unicode
from django.utils.functional import Promise

from ajax_forms.ajax_fields import factory as field_factory

__all__ = (
    'form_to_json', 'LazyEncoder',
)


class LazyEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

json_serializer = LazyEncoder()


def form_to_json(form):
    # Generate ajax fields
    ajax_fields = []
    for name, field in form.fields.items():
        ajax_field = field_factory(field, name)
        ajax_fields.append(ajax_field.to_ajax())
    return json_serializer.encode(ajax_fields)
