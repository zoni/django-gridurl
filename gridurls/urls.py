from django.conf.urls.defaults import *

urlpatterns = patterns('gridurls.views',
    (r'^$', 'index'),
    (r'^register$', 'register'),
    (r'^update/([\w-]*)', 'update'),
    (r'^get/([\w-]*)', 'get'),
    (r'^go/([\w-]*)', 'go'),
    # The next one basically duplicates the /go/<name> so /<name> directly works too
    # It must be at the bottom though as entries are matched in order
    (r'^([\w-]*)', 'go'),
)
