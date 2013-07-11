from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WCDB.views.home', name='home'),
    # url(r'^WCDB/', include('WCDB.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^wcdb/$', 'wcdb.views.index'),
    url(r'^wcdb/static2/', 'wcdb.views.static_two'),
    url(r'^test/$', 'wcdb.views.run_tests'),
    url(r'^login/$', 'wcdb.views.my_login'),
    url(r'^upload/$', 'wcdb.views.upload_file'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
