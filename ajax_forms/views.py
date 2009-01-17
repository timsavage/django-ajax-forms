from django.http import HttpResponse
from django.views.decorators.http import require_POST

from ajax_forms.utils import LazyEncoder


@require_POST
def validate(request, field, form):
    return HttpResponse('not implimented', status=500, mimetype="text/plain")


def validate_secure(request, *args, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponse('authentication required', status=401,
            mimetype="text/plain")
    return validate(request, *args, **kwargs)
