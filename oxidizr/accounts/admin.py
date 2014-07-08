from django.contrib import admin

from .models import User, EmailVerificationCode, PasswordResetCode


admin.site.register([User, EmailVerificationCode, PasswordResetCode])