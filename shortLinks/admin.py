from django.contrib import admin

from shortLinks.models import Links

class ShorterAdmin(admin.ModelAdmin):
    readonly_fields = ['links_short', 'links_http', 'links_count', 'links_login']
    list_filter = ['links_login']
    list_display = ['links_short', 'links_http', 'links_count', 'links_login']


admin.site.register(Links, ShorterAdmin)
