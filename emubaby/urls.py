from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from tastypie.api import Api
from datastore.api import *

api = Api(api_name='v1')
api.register(BuildResource())
api.register(MetaDataCategoryResource())
api.register(MetaDataResource())
api.register(ArtifactTypeResource())
api.register(ArtifactResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/', include(api.urls)),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
