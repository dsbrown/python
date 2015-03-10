#IPSGO urls
#
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ipsgo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^site/', include('site_selection.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
