

# Introduction #

This document documents the format of field definitions that are produced from introspecting your Django `Form`.


# Field structure #

Example (_has been formatted with newline and tab characters_):
```
"example": {
    "required": true,
    "msgs": {
        "max_length": "Ensure this value has at most %(max)d characters (it has %(length)d).", 
        "required": "This field is required."
    },
    "rules": {
        "max_length": 30
    }
}
```
The dictionary key is used to pass the fields name, this corresponds to the `name` attribute on an HTML `input` or `textarea` field.

## Properties ##
<table>
<tr><td><b>required</b></td><td>Boolean</td></tr>
<tr><td>This field is required to be filled in.</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>msgs</b></td><td>Object</td></tr>
<tr><td>Dictionary of error messages.</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>rules</b></td><td>Array</td></tr>
<tr><td>Dictionary of rules that must be met by field value. See <a href='#Rules'><i>Rules</i></a> section</td></tr>
<tr><td>

<hr />

</td></tr>
</table>
<br />

# Rules #
Since many of the checks done during cleaning of your form data are very similar they are implimented as a series of "rules", basically functions that take the form value  and an argument.

## Built-in rules ##

### Field rules ###
<table>
<tr><td><b>min_length</b>/<b>max_length</b></td><td><i>Integer</i></td><td>Error Message key: <i>min_length</i>/<i>max_length</i></td></tr>
<tr><td>Ensure that the field values lengthis within the defined range.</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>decimal_lengths</b></td><td>(<i>Integer</i>, <i>Integer</i>)</td><td>Error Message key: <i>max_digits</i>, <i>max_decimal_places</i>, <i>max_whole_digits</i></td></tr>
<tr><td>Ensure that numbers decimal and whole parts are within range.<br />
Argument for a decimal_lengths rule is a "tuple" (or list in JSON terminology). The first item is the maximum number of digits; the second is the maximum of decimal places.</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>is_float</b></td><td><i>Boolean</i></td><td>Error Message key: <i>invalid</i></td></tr>
<tr><td>Ensure the field can be cast to a float type.</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>is_integer</b></td><td><i>Boolean</i></td><td>Error Message key: <i>invalid</i></td></tr>
<tr><td>Ensure the field can be cast to a integer type.</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>is_date</b></td><td><i>Boolean</i></td><td>Error Message key: <i>invalid</i></td></tr>
<tr><td>
Ensure the field value matches a Django date field. <br />
Note: This validation is not complete, only validates numerical formats.<br>
</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>is_datetime</b></td><td><i>Boolean</i></td><td>Error Message key: <i>invalid</i></td></tr>
<tr><td>Ensure the field value matches a Django date time field type.</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>is_time</b></td><td><i>Boolean</i></td><td>Error Message key: <i>invalid</i></td></tr>
<tr><td>Ensure the field value matches a Django time field.</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>min_value</b>/<b>max_value</b></td><td><i>Number</i></td><td>Error Message key: <i>min_value</i>/<i>max_value</i></td></tr>
<tr><td>Ensure that the field value is within the defined range.</td></tr>
<tr><td>

<hr />

</td></tr>

<tr><td><b>regex</b></td><td>(<i>String</i>, <i>String</i>)</td><td>Error Message key: <i>invalid</i></td></tr>
<tr><td>
Ensure the field value matches a regular expression.<br />
Argument for a regex rule is a "tuple" (or list in JSON terminology). The first item is the regular expression itself; the second are flags to use with the regular expression.<br>
</td></tr>
<tr><td>

<hr />

</td></tr>
</table>

### Form rules ###
Rules that are applied at the form level (see ExtendingForms for details).
<table>
<tr><td><b>equal_to_field</b></td><td><i>String</i></td><td>Error Message key: <i>equal_to_field</i></td></tr>
<tr><td>Ensure that this field is equal to another field in the form. Example being password and password check fields.</td></tr>
<tr><td>

<hr />

</td></tr>
</table>
<br />
At this time dates formats are not being checked.

## Custom Rules ##

Custom rules are supported by both the server side Python code and the client side [JavaScript](JavascriptComponent.md) (jQuery) code. See the associated documentation (once it has been written) for information on adding custom rule.