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
    url(r'^static1/$', 'wcdb.views.static_one'),
    url(r'^static2/$', 'wcdb.views.static_two'),
    url(r'^static3/$', 'wcdb.views.static_three'),
    url(r'^static4/$', 'wcdb.views.static_four'),
    url(r'^static5/$', 'wcdb.views.static_five'),
    url(r'^static6/$', 'wcdb.views.static_six'),
    url(r'^static7/$', 'wcdb.views.static_seven'),
    url(r'^static8/$', 'wcdb.views.static_eight'),
    url(r'^static9/$', 'wcdb.views.static_nine'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
