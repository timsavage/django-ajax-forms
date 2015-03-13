# Client side JavaScript validation for any Django form. #

Updates!

Has been a long time since an update has been made, but I'm back building Django applications and this library is once again becoming very useful in my day to day development.

  * Caching support has been added.
  * With the support of caching I have also solved some of the issues I was having getting call back validation to work. As this is the most requested feature it will now be my focus in the coming weeks.

More soon.

Issues with Django 1.2: There have been changes in newforms validation inclued in django 1.2. See [this issue](http://code.google.com/p/django-ajax-forms/issues/detail?id=11) for more information.

A branch has been started for a release for 1.2 to allow for backwards compatibility with previous Django releases. An initial update has been added to the 1.2 branch, this update allows forms to work with Django 1.2. The branch can be fetched from [here](http://code.google.com/p/django-ajax-forms/source/browse/?r=02cec0f1879c75d106201161e7d4056a92dbc1d3).

Now on PyPi http://pypi.python.org/pypi/django-ajax-forms/

## Features ##
See the UpcomingFeatures wiki page for more details of some of these features.
  * Template tag to provide JavaScipt (JSON) field description of any Django form via introspection.
  * Extended attributes defined on the form (similar to inner `Meta` classs)
    * Custom validation, similar to how `clean` is used in `Form` classes
    * Comparison between fields (ie compare password and password check fields)
  * Support for custom fields (ie fields that are not part of the Django distribution)
  * Output form using a `<dl>` structure
  * Caching of generated JSON. Uses the built in caching framework to cache generated JSON.

## Planned Features ##
In order of priority:
  * AJAX callbacks for validation that requires server interaction (ie check that a username is not already in use)
  * Enhancements jQuery validation lib
    * Grouped error messages
    * Greater control over css classes
  * Tests!

## Dependencies & Compatibility ##
  * Python 2.4+
  * Django 1.0.2+
  * jQuery 1.2.6 (optional, the reference implementation has been developed with jQuery)

## Simple Examples ##
A [complete example](http://code.google.com/p/django-ajax-forms/source/browse/#hg/example) is included in the source repository and includes several samples of the library in use.

A basic example of usage:
```
{% load ajax_form_utils %}

<form method="post">
  <table>
    {{ form.as_table }}
    <tr><td></td><td><input type="submit" /></td></tr>
  </table>
</form>

<script type="text/javascript">
    $(function(){
        $('form').validation({% render_ajax_fields form %});
    });
</script>
```

With DL rendering:
```
{% load ajax_form_utils %}

<form method="post">
  <dl>
    {{ as_dl form }}
    <dd><input type="submit" /></dd>
  </dl>
</form>

<script type="text/javascript">
    $(function(){
        $('form').validation({% render_ajax_fields form %}, {
            layout: 'dl'
        });
    });
</script>
```