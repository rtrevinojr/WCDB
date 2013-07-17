from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from wcdb import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cache_money.views.home', name='home'),
    # url(r'^cache_money/', include('cache_money.foo.urls')),
    url(r'^wcdb/export/$', views.export_prompt),
    url(r'^wcdb/export/raw/$', views.export_raw),
    url(r'^wcdb/export/download/$', views.export_download),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': cache_money.settings.MEDIA_ROOT}),
    url(r'^wcdb/$', TemplateView.as_view(template_name='index.html'), name="wcdb"),
    url(r'^wcdb/org/$', TemplateView.as_view(template_name='org.html'), name="org"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

	# leave off  wcdb
    url(r'^(home)?/?$', TemplateView.as_view(template_name='index.html'), name="wcdb"),
)
