from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseKeyword(models.Model):
    """
    This model holds all the keywords in the system. Best efforts are made to keep this list clean.
    Text is cleaned using various methods to mitigate mistakes.

    Keywords must follow these rules:
    * can be only in lower case.
    * may not have a comma (multiple keywords not allowed)
    """
    term = models.CharField(max_length=60, blank=False, null=False, unique=True)

    def clean_term(self):
        term = self.cleaned_data['term']
        return term.strip().lower().replace(',', '')


class KeywordSettings(object):
    KEYWORD_ENABLED = 1
    KEYWORD_DISABLED = 2
    KEYWORD_EXCLUDED = 4
    KEYWORD_MANDATORY = 8

KEYWORD_SETTINGS_CHOICES = (
    (KeywordSettings.KEYWORD_ENABLED, _('Enabled in results')),
    (KeywordSettings.KEYWORD_DISABLED, _('Ignored is results')),
    (KeywordSettings.KEYWORD_EXCLUDED, _('Exclude from results')),
    (KeywordSettings.KEYWORD_MANDATORY, _('Must exist in results'))
)


class Keyword(models.Model):
    """
    This model holds the keyword data, related per affiliate.
    Also for every (keyword, affiliate) pair there are settings for the actual usage of the keywords.

    The settings allow users to control how the keywords play in search filtering.
    """
    keyword = models.ForeignKey('keywords.BaseKeyword', related_name='+')
    affiliate = models.ForeignKey('affiliates.Affiliate', related_name='keywords')

    # This meta contains JSON encoded status for each application that needs keywords to filter search results
    # TODO: Allow keywords to be combined in search filter. Basically keyword dependencies.
    status_settings_meta = models.CharField(max_length=500, blank=True, null=True)