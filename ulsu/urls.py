from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core.views import login
from core.views import logout

admin.autodiscover()

urlpatterns = staticfiles_urlpatterns() + patterns('',
    url(r'^admin/core/node/', 'core.views.node_tree'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url('', include('core.urls')),
)