from django import template

from ajax_forms.utils import form_to_json

register = template.Library()


class RenderAjaxFieldsNode(template.Node):

    def __init__(self, form):
        self.form = template.Variable(form)

    def render(self, context):
        form = self.form.resolve(context)
        return form_to_json(form)


@register.tag
def render_ajax_fields(parser, token):
    """
    This will render a Django form into an ajax.

    Usage::

        {% load ajax_form_tools %}
        {% render_ajax_form form %}

    """
    try:
        tag_name, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument"
            % token.contents.split()[0])
    return RenderAjaxFieldsNode(form)
