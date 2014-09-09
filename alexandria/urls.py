from django.conf.urls import patterns, include, url
from django.contrib import admin
from datastore import views
from datastore.creation import BuildNotification
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'builds', views.BuildViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'metadata-categories', views.MetadataCategoryViewSet)
router.register(r'metadata', views.MetadataValueViewSet)
router.register(r'artifact-categories', views.ArtifactCategoryViewSet)


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'build/$', BuildNotification.as_view()),
)
