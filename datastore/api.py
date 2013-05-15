from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from datastore.models import *
from django.db.models import Q
from datastore.utils import get_build_query_set


class EmuBabyResource(ModelResource):
	def determine_format(self, request):
		return 'application/json'


class BuildResource(EmuBabyResource):
	def apply_filters(self, request, applicable_filters):
		base_list = super(BuildResource, self).apply_filters(request, applicable_filters)

		q_list = get_build_query_set(request.GET, base_list)

		if q_list is None:
			return base_list
		else:
			return q_list


	class Meta:
		queryset = Build.objects.all()
		resource_name = 'build'


class MetaDataCategoryResource(EmuBabyResource):
	class Meta:
		queryset = MetaDataCategory.objects.all()
		resource_name = 'metadatacategory'
		filtering = {
			'slug': ALL
		}


class MetaDataResource(EmuBabyResource):
	def apply_filters(self, request, applicable_filters):
		base_list = super(MetaDataResource, self).apply_filters(request, applicable_filters)
		if request.GET.get('distinct', None):
			return base_list.distinct('value')
		else:
			return base_list


	category = fields.ForeignKey(MetaDataCategoryResource, 'category')
	class Meta:
		queryset = MetaData.objects.all()
		resource_name = 'metadata'
		filtering = {
			'category': ALL_WITH_RELATIONS
		}


class ArtifactTypeResource(EmuBabyResource):
	class Meta:
		queryset = ArtifactType.objects.all()
		resource_name = 'artifacttype'


class ArtifactResource(EmuBabyResource):
	a_type = fields.ForeignKey(ArtifactTypeResource, 'a_type')
	class Meta:
		queryset = Artifact.objects.all()
		resource_name = 'artifact'
		filtering = {
			'a_type': ALL_WITH_RELATIONS
		}
