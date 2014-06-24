from django.contrib import admin

from .models import Keyword, Event


admin.site.register([Keyword, Event])