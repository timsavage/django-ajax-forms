from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^1/$', 'foo.views.example1', name='example1'),
    url(r'^2/$', 'foo.views.example2', name='example2'),
    url(r'^3/$', 'foo.views.example3', name='example3'),
    url(r'^4/$', 'foo.views.example4', name='example4'),
)
