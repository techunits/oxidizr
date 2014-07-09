# Imports from system
import datetime

# Imports from Django
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from crispy_forms.bootstrap import PrependedText, AppendedText


User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('Email Address'), max_length=75, widget=forms.TextInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_form_accounts_login'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('email', tabindex=1),
                    css_class='col-sm-6 col-sm-offset-3'
                ),
                Div(
                    Field('password', tabindex=2),
                    css_class='col-sm-6 col-sm-offset-3'
                ),
                Div(
                    HTML('''<a href="{% url 'accounts_forgot_password' %}">{{ _('I forgot the password') }}</a>'''),
                    css_class='col-sm-6 col-sm-offset-3'
                ),
                css_class='row'
            ),
            HTML('''<hr class="full">'''),
            Div(
                Div(
                    HTML('''<a href="{% url 'welcome_page' %}"> {{ _('Cancel') }}</a>&nbsp;&nbsp;'''),
                    Submit('submit', _('Login'), css_class='btn-success btn-lg'),
                    css_class='pull-right'
                ),
                css_class='row',
            )
        )


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'tabindex': 1}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'tabindex': 2}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'tabindex': 8}), label=_('Repeat Password'),
                                      required=True)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_form_register'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('first_name', tabindex=1),
                    css_class='col-sm-6'
                ),
                Div(
                    Field('last_name', tabindex=2),
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('username', tabindex=3),
                    css_class='col-sm-6'
                ),
                Div(
                    Field('email', tabindex=4),
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('password', tabindex=5),
                    css_class='col-sm-6'
                ),
                Div(
                    Field('repeat_password', tabindex=6),
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
            'username': forms.TextInput(),
            'email': forms.TextInput(),
            'password': forms.PasswordInput(),
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


class EmailVerificationForm(forms.Form):
    code = forms.CharField(max_length=10, label=_('Verification code in email'), required=True)
    _verification_code = None
    _email_token = None

    def __init__(self, *args, **kwargs):
        self._email_token = kwargs.pop('email_token', None)
        self._verification_code = self._email_token.verification_code
        super(EmailVerificationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_form_email_verification'
        self.helper.form_action = reverse_lazy('accounts_email_verification', args=(self._email_token.id,))
        self.helper.layout = Layout(
            Div(
                'code',
            ),
            HTML('''<hr class="full">'''),
            Div(
                Div(
                    HTML('''<a href="{% url 'accounts_register' %}">
                    {{ _('Cancel and sign up again') }}</a>&nbsp;&nbsp;'''),
                    Submit('submit', _('Verify Email address'), css_class='btn-success btn-lg'),
                    css_class='pull-right'
                )
            )
        )

    def clean_code(self):
        code = self.cleaned_data['code']
        if self._verification_code and code != self._verification_code:
            raise forms.ValidationError(_('The code did not match what we sent you in Email.'))
        return code


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_form_forgot_password'
        self.helper.layout = Layout(
            Div(
                'email',
            ),
            HTML('''<hr class="full">'''),
            Div(
                Div(
                    HTML('''<a href="{% url 'accounts_login' %}"> {{ _('Cancel and login') }}</a>&nbsp;&nbsp;'''),
                    Submit('submit', _('Continue'), css_class='btn-success btn-lg'),
                    css_class='pull-right'
                )
            )
        )


class ResetPasswordForm(forms.Form):
    verification_code = forms.CharField(help_text=_('The verification code we sent you in email.'),
                                        max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label=_('New password'), required=True)
    repeat_password = forms.CharField(widget=forms.PasswordInput, label=_('Confirm password'), required=True)

    def clean_password(self):
        return self.cleaned_data['password'].strip()

    def clean_repeat_password(self):
        return self.cleaned_data['repeat_password'].strip()

    def clean(self):
        data = super(ResetPasswordForm, self).clean()
        if data['password'] != data['repeat_password']:
            raise forms.ValidationError(
                _('Passwords do not match.'),
                code='invalid'
            )
        return data

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_form_reset_password'
        self.helper.layout = Layout(
            Div(
                'verification_code',
                'password',
                'repeat_password',
            ),
            HTML('''<hr class="full">'''),
            Div(
                Div(
                    HTML('''<a href="{% url 'accounts_login' %}"> {{ _('Cancel and login') }}</a>&nbsp;&nbsp;'''),
                    Submit('submit', _('Reset password'), css_class='btn-success btn-lg'),
                    css_class='pull-right'
                )
            )
        )