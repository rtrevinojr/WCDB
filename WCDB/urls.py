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
    url(r'^wcdb/import/$', 'wcdb.views.import_file'),
    url(r'^wcdb/export/$', 'wcdb.views.export_file', name='export'),

    url(r'^wcdb/China_Maritime_Conflict_page.html', 'wcdb.views.chinamaritime'),
    url(r'^wcdb/Human_Trafficking_page.html', 'wcdb.views.humantrafficking'),
    url(r'^wcdb/North_Korean_Conflict_page.html', 'wcdb.views.northkorea'),

    url(r'^wcdb/John_Kerry_page.html', 'wcdb.views.johnkerry'),
    url(r'^wcdb/Mohamed_Morsi_page.html', 'wcdb.views.mohamedmorsi'),
    url(r'^wcdb/Ricky_Martin_page.html', 'wcdb.views.rickymartin'),

    url(r'^wcdb/ASEAN_page.html', 'wcdb.views.asean'),
    url(r'^wcdb/BNP_Paribas_page.html', 'wcdb.views.bnpparibas'),
    url(r'^wcdb/Polaris_Project_page.html', 'wcdb.views.polaris'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
