# Imports from Django core
from django import forms
from django.utils.translation import ugettext_lazy as _

# Imports from third party Django libs
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from crispy_forms.bootstrap import PrependedText, AppendedText

# Imports from our custom apps

# Explicit imports from this app
from .models import BaseKeyword


class KeywordCreateForm(forms.Form):
    term = forms.CharField(max_length=60, required=True)

    def __init__(self, *args, **kwargs):
        super(KeywordCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_form_keywords_create'
        self.helper.layout = Layout(
            Div(
                Div(
                    'term',
                    css_class='col-sm-6 col-sm-offset-3'
                ),
                css_class='row'
            ),
            HTML('''<hr class="full">'''),
            Div(
                Div(
                    HTML('''<a href="{% url 'keywords_manage' %}">{{ _('Cancel') }}</a>&nbsp;&nbsp;'''),
                    Submit('submit', _('Save'), css_class='btn-success btn-lg'),
                    css_class='pull-right'
                ),
                css_class='row',
            )
        )

    def clean_term(self):
        term = self.cleaned_data['term']
        return term.strip().lower().replace(',', '')