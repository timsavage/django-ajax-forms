from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import Example1, Example2, Example3, Example4


def example1(request, form_class=Example1,
        template_name="foo/example1.html"):
    message = None
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            message = "OK"
    else:
        form = form_class()
    return render_to_response(template_name, {
        "form": form,
        "message": message,
    }, context_instance=RequestContext(request))


def example2(request, form_class=Example2,
        template_name="foo/example2.html"):
    message = None
    if request.method == "POST":
        form = form_class(request.POST, prefix="test")
        if form.is_valid():
            message = "OK"
    else:
        form = form_class(prefix="test")
    return render_to_response(template_name, {
        "form": form,
        "message": message,
    }, context_instance=RequestContext(request))


def example3(request, form_class=Example3,
        template_name="foo/example3.html"):
    message = None
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            message = "OK"
    else:
        form = form_class()
    return render_to_response(template_name, {
        "form": form,
        "message": message,
    }, context_instance=RequestContext(request))


def example4(request, form_class=Example4,
        template_name="foo/example4.html"):
    message = None
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            message = "OK"
    else:
        form = form_class()
    return render_to_response(template_name, {
        "form": form,
        "message": message,
    }, context_instance=RequestContext(request))
