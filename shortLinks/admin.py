from django.contrib import admin

from shortLinks.models import Link


class ShorterAdmin(admin.ModelAdmin):
    readonly_fields = [
        'short', 'full',
        'count', 'login'
    ]
    list_display = [
        'short', 'full',
        'count', 'login'
    ]
    list_filter = ['login']

admin.site.register(Link, ShorterAdmin)
