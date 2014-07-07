# Imports from system
import datetime

# Imports from Django
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from crispy_forms.bootstrap import PrependedText, AppendedText


User = get_user_model()


# class ResetPasswordForm(forms.ModelForm):
#     repeat_password = forms.CharField(widget=forms.PasswordInput, label=_('Repeat Password'))
#
#     class Meta:
#         model = User
#         fields = ('password',)
#         widgets = {
#             'password': forms.PasswordInput()
#         }


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('Email Address'), max_length=75, widget=forms.TextInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'tabindex': 1}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'tabindex': 2}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'tabindex': 8}), label=_('Repeat Password'),
                                      required=True)
    date_of_birth = forms.DateField(input_formats=[settings.DATE_FORMAT_PYTHON])

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_form_register'
        self.helper.layout = Layout(
            Div(
                Div(
                    'first_name',
                    css_class='col-sm-6'
                ),
                Div(
                    'last_name',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    'username',
                    css_class='col-sm-6'
                ),
                Div(
                    'email',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    'password',
                    css_class='col-sm-6'
                ),
                Div(
                    'repeat_password',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            HTML('''<hr class="full">'''),
            Div(
                Div(
                    HTML('''<a href="{% url 'home_page' %}">
                    {{ _('Cancel and return to home page') }}</a>&nbsp;&nbsp;'''),
                    Submit('submit', _('Save and continue'), css_class='btn-success btn-lg'),
                    css_class='pull-right'
                ),
                css_class='row',
            )
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'repeat_password')
        widgets = {
            'username': forms.TextInput(attrs={'tabindex': 3}),
            'email': forms.TextInput(attrs={'tabindex': 4}),
            'password': forms.PasswordInput(attrs={'tabindex': 7}),
        }

    def clean(self):
        super(RegistrationForm, self).clean()
        if 'password' in self.cleaned_data and 'repeat_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
                raise forms.ValidationError(
                    _('Passwords do not match.'),
                    code='invalid'
                )
        return self.cleaned_data


# class ForgotRequestForm(forms.ModelForm):
#     class Meta:
#         model =
#         fields = ('email',)


class EmailVerificationForm(forms.Form):
    code = forms.CharField(max_length=10, label=_('Verification code in email'), required=True)
    _user_code = None

    def __init__(self, *args, **kwargs):
        self._user_code = kwargs.pop('user_code', None)
        super(EmailVerificationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_form_email_verification'
        self.helper.layout = Layout(
            Div(
                'code',
            ),
            HTML('''<hr class="full">'''),
            Div(
                Div(
                    HTML('''<a href="{% url 'register' %}">
                    {{ _('Cancel and sign up again') }}</a>&nbsp;&nbsp;'''),
                    Submit('submit', _('Verify Email address'), css_class='btn-success btn-lg'),
                    css_class='pull-right'
                )
            )
        )

    def clean_code(self):
        code = self.cleaned_data['code']
        if self._user_code and code != self._user_code:
            raise forms.ValidationError(_('The code did not match what we sent you in Email.'))
        return code