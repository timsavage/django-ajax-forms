from decimal import Decimal
from django import forms

class Example1(forms.Form):
    CHOICES = (
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
    )

    boolean = forms.BooleanField(label='BooleanField')
    charfield = forms.CharField(label='CharField', max_length=30, min_length=3)
    choicefield = forms.ChoiceField(label='ChoiceField', choices=CHOICES)
    typedchoicefield = forms.TypedChoiceField(label='TypedChoiceField', choices=CHOICES, empty_value=0, coerce=int)
    datefield = forms.DateField(label='DateField')
    datetimefield = forms.DateTimeField(label='DateTimeField')
    decimalfield = forms.DecimalField(label='DecimalField', max_value=Decimal('2291.3321'), min_value=Decimal('432.3244'), max_digits=9, decimal_places=4)
    emailfield = forms.EmailField(label='EmailField')
    #filefield = forms.FileField(label='FileField')
    floatfield = forms.FloatField(label='FloatField', max_value=23.6, min_value=-5.32)
    integerfield = forms.IntegerField(label='IntegerField', max_value=66, min_value=22)
    ipaddressfield = forms.IPAddressField(label='IPAddressField')
    multiplechoicefield = forms.MultipleChoiceField(label='MultipleChoiceField', choices=CHOICES)
    nullbooleanfield = forms.NullBooleanField(label='NullBooleanField')
    regexfield = forms.RegexField(label='RegexField', regex=r'^[\w\.\-]+$', error_messages={
        'invalid': 'Value may only contain letters, numbers, fullstop and dash'})
    timefield = forms.TimeField(label='TimeField')
    urlfield = forms.URLField(label='URLField')

class Example2(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput())
    password1 = forms.CharField(label='New Password', min_length=6, widget=forms.PasswordInput(),
        help_text = "at least 6 characters (case sensitive)")
    password2 = forms.CharField(label='New Password (again)', required=True, widget=forms.PasswordInput())

    class Ajax:
        rules = [
            ('password2', {'equal_to_field': 'password1'})
        ]
        messages = [
            ('password2', {'equal_to_field': "Password fields didn't match."})
        ]


class Example3(forms.Form):
    username = forms.RegexField(max_length=30, regex=r'^[\w\.\-]+$',  widget=forms.TextInput(),
        help_text = "Alphanumeric value must with at most 30 characters",
        error_message = "This value must contain only letters, numbers and underscores.")
    email = forms.EmailField(label="E-mail", widget=forms.TextInput())
    password1 = forms.CharField(label='New Password', min_length=6, widget=forms.PasswordInput(),
        help_text = "at least 6 characters (case sensitive)")
    password2 = forms.CharField(label='New Password (again)', required=True, widget=forms.PasswordInput())

    class Ajax:
        callback_url = 'ajax_example3'
        callback_fields = ['username', 'email']
        rules = [
            ('password2', {'equal_to_field': 'password1'})
        ]
        messages = [
            ('password2', {'equal_to_field': "Password fields didn't match."})
        ]

    def clean_username(self):
        pass

    def clean_email(self):
        pass


class Example4(forms.Form):
    pass
