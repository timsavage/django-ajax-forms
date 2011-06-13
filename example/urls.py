from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^foo/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Catch all
    url(r'test/', 'django.views.generic.simple.direct_to_template', {"template": "foo/test.html"}),
    url(r'^.*', 'django.views.generic.simple.direct_to_template', {"template": "foo/home.html"}),
)
