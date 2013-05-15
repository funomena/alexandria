from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from tastypie.api import Api
from datastore.api import *
import frontend.views

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
	url(r'^$', frontend.views.index, name='index'),
	url(r'^latest/', frontend.views.latest, name='latest'),
	url(r'^build/(?P<build_id>\d*)/', frontend.views.build_page, name='build'),
    (r'^api/', include(api.urls)),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	(r'accounts/', include('registration.backends.default.urls')),
	(r'accounts/profile/', frontend.views.profile_page)
)
