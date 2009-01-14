from django import template

from ajax_forms.utils import form_to_json

register = template.Library()


class RenderFormValidationNode(template.Node):

    def __init__(self, form):
        self.form = template.Variable(form)

    def render(self, context):
        form = self.form.resolve(context)
        return form_to_json(form)


@register.tag
def render_form_fields(parser, token):
    try:
        tag_name, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return RenderFormValidationNode(form)
