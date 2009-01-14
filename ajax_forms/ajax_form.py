from ajax_forms.utils import LazyEncoder
from ajax_forms.ajax_fields import factory as field_factory

__all__ = (
    'form_to_json'
)

json_serializer = LazyEncoder()


def form_to_json(form):
    data = []
    for name, field in form.fields.items():
        ajax_field = field_factory(field)
        data.append({'name': form.add_prefix(name), 'validators': ajax_field.validators})
    return json_serializer.encode(data)
