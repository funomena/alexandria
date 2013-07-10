from django.conf.urls import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tastypie.api import Api
from datastore.api import *
import frontend.views

api = Api(api_name='v0')
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
	url(r'^builds/', frontend.views.build_list_page, name='build list'),
	url(r'^filter/', frontend.views.build_filter_page, name='build filter'),
	url(r'^download/(?P<a_id>\d*)/', frontend.views.artifact_download_redirect, name='download artifact'),
	url(r'^download/(?P<a_id>\d*)/', datastore.uploads.artifact_download_redirect, name='download artifact'),
    (r'^api/', include(api.urls)),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	(r'accounts/', include('registration.backends.default.urls')),
	(r'accounts/profile/', frontend.views.profile_page)
)

urlpatterns += staticfiles_urlpatterns()