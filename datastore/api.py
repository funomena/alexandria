from tastypie.resources import ModelResource
from datastore.models import *


class BuildResource(ModelResource):
	class Meta:
		queryset = Build.objects.all()
		resource_name = 'build'


class MetaDataCategoryResource(ModelResource):
	class Meta:
		queryset = MetaDataCategory.objects.all()
		resource_name = 'metadatacategory'


class MetaDataResource(ModelResource):
	class Meta:
		queryset = MetaData.objects.all()
		resource_name = 'metadata'


class ArtifactTypeResource(ModelResource):
	class Meta:
		queryset = ArtifactType.objects.all()
		resource_name = 'artifacttype'


class ArtifactResource(ModelResource):
	class Meta:
		queryset = Artifact.objects.all()
		resource_name = 'artifact'
