from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^foo/', include('example.foo.urls')),

    # Trick for Django to support static files (security hole: only for Dev environement! remove this on Prod!!!)
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Catch all
    url(r'test/', 'django.views.generic.simple.direct_to_template', {"template": "foo/test.html"}),
    url(r'^.*', 'django.views.generic.simple.direct_to_template', {"template": "foo/home.html"}),
)
