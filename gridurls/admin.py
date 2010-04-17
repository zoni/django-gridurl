from django.contrib import admin
from gridurls.models import Url

class UrlAdmin(admin.ModelAdmin):
    pass
admin.site.register(Url, UrlAdmin)

