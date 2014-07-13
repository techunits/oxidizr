# Imports from Django core
from django import forms
from django.utils.translation import ugettext_lazy as _

# Imports from third party Django libs
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from crispy_forms.bootstrap import PrependedText, AppendedText

# Imports from our custom apps

# Explicit imports from this app
from .models import APIKey


class CreateKeyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_form_twitter_auth_token'
        self.helper.layout = Layout(
            Div(
                HTML('''<h4>{{ _('Application settings') }}</h4>'''),
                Div(
                    'api_key',
                    css_class='col-sm-6'
                ),
                Div(
                    'api_secret',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                HTML('''<h4>{{ _('Your access token') }}</h4>'''),
                Div(
                    'consumer_key',
                    css_class='col-sm-6'
                ),
                Div(
                    'consumer_secret',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            HTML('''<hr class="full">'''),
            Div(
                Div(
                    HTML('''<a href="{% url 'twitter_index' %}">{{ _('Cancel') }}</a>&nbsp;&nbsp;'''),
                    Submit('submit', _('Save'), css_class='btn-success btn-lg'),
                    css_class='pull-right'
                ),
                css_class='row',
            )
        )

    class Meta:
        model = APIKey
        fields = ['api_key', 'api_secret', 'consumer_key', 'consumer_secret']