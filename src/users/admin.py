from django.contrib import admin

from users.models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
