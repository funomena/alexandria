from django.conf.urls import patterns, include, url
from django.contrib import admin
from datastore import views
from datastore.artifact_handlers import ArtifactUpload, download_url_redirect
from datastore.build_handlers import BuildNotification
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'builds', views.BuildViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'metadata-categories', views.MetadataCategoryViewSet)
router.register(r'metadata', views.MetadataValueViewSet)
router.register(r'artifact-categories', views.ArtifactCategoryViewSet)


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'api/build/$', BuildNotification.as_view()),
    url(r'api/artifact/$', ArtifactUpload.as_view()),
    url(r'download/(?P<pk>[0-9]+)/$', download_url_redirect)
)
