from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from datastore.models import *
from django.db.models import Q


class BuildResource(ModelResource):
	def apply_filters(self, request, applicable_filters):
		base_list = super(BuildResource, self).apply_filters(request, applicable_filters)

		q_list = []
		all_meta_cats = MetaDataCategory.objects.all()
		for meta_cat in all_meta_cats:
			meta_value = request.GET.get(meta_cat.slug, None)
			if meta_value:
				q_subset = 	Q(metadata__category__slug = meta_cat.slug, metadata__value = meta_value)
						
				q_list.append(base_list.filter(q_subset).distinct())

		q_string = ""
		for i in range(0, len(q_list) - 1):
			q_string += "q_list[" + str(i) + "] & "
		q_string += "q_list[" + str(len(q_list) - 1) + "]"

		if len(q_list) == 0:
			return base_list
		else:
			return eval(q_string)


	class Meta:
		queryset = Build.objects.all()
		resource_name = 'build'


class MetaDataCategoryResource(ModelResource):
	class Meta:
		queryset = MetaDataCategory.objects.all()
		resource_name = 'metadatacategory'


class MetaDataResource(ModelResource):
	category = fields.ForeignKey(MetaDataCategoryResource, 'category')
	class Meta:
		queryset = MetaData.objects.all()
		resource_name = 'metadata'
		filtering = {
			'category': ALL_WITH_RELATIONS
		}


class ArtifactTypeResource(ModelResource):
	class Meta:
		queryset = ArtifactType.objects.all()
		resource_name = 'artifacttype'


class ArtifactResource(ModelResource):
	a_type = fields.ForeignKey(ArtifactTypeResource, 'a_type')
	class Meta:
		queryset = Artifact.objects.all()
		resource_name = 'artifact'
		filtering = {
			'a_type': ALL_WITH_RELATIONS
		}
