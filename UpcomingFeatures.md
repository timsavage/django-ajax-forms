I have received a number of emails regarding some of the my planned features, this page is intended to expand on those features and to give an overview of the intended implementation.



# AJAX callbacks #

One of my design goals for this application is for all server side validation code to remain encapsulated within existing Django Form's. With this in mind any callbacks to validate a particular field must use the same methods for validation including any clean methods that have been defined by the developer.

This application was partially inspired by Alex Gaynor's [django-ajax-validation](http://github.com/alex/django-ajax-validation/tree/master) application and the AJAX callback component will be implemented in a similar fashion. django-ajax-validation though has a couple of drawbacks, namely:
  * No concept of security - cannot require a login or particular permission.
  * Is all or nothing - The entire form is validated at callback not just a single field this produces problems if you have multiple fields that require server callbacks (ie username and unique email on a sign up form).

## Form Definition ##

AJAX callbacks should be defined using the existing `Meta` class analogy already employed to provided extended validation. For example:
```
class Foo(forms.Form):

    username = forms.CharField(min_length=3)
    password1 = forms.CharField(label='New Password', min_length=6, widget=forms.PasswordInput(render_value=False),
        help_text = "at least 6 characters (case sensitive)")
    password2 = forms.CharField(label='New Password (again)', required=False, widget=forms.PasswordInput(render_value=False))

    class Ajax:
        ajax_url = '/Forms/Foo'
        rules = [
            ('username', {'ajax_callback': ''})
            ('password2', {'equal_to_field': 'password1'})
        ]
        messages = [
            ('password2', {'equal_to_field': "Password fields didn't match."})
        ]
```

## View Definition ##

As in django-ajax-validation views should be defined in urls.py with the form to be validated passed to the view. This allows for the validation view to be defined generically. Extending on this idea a "secure" version of the validation view should be provided to enforce that the current site user has rights to use the form validation (ie to prevent the validation being used to find confirm any information stored within your application).

Example:
```
urlpatterns = patterns('',
    url(r'^Foo/', 'ajax_forms.views.validate', {"form": Foo}),
    url(r'^FooAlt/', 'ajax_forms.views.secure_validate', {"form": 'my_project.forms.Foo'}),
)
```

All validation request data must be sent via HTTP POST requests to prevent XSS attacks.

## AJAX Code ##

An update will be required to the AJAX definition code to pass through the additional url. Some modification will be required for the client side code to allow for the async nature of validation requests.

# Caching of generated JSON #

Generated JSON code should not change over the lifetime of a form so this presents a good use-case for caching the resulting JSON.

The options for this include storing the generated JSON against the from class itself or storing the result with the built in Django caching features. I'm leaning towards the later implementation as it provides more configurable solution to the developer, of course the method of caching could also be configured with storing against the Form itself an option.