from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Comment the next line to disable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('gridurls.urls')),
)
