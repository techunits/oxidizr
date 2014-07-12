from django.contrib import admin

from .models import BaseKeyword, Keyword


admin.site.register([BaseKeyword, Keyword])