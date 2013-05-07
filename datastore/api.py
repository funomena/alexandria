from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from datastore.models import *
from django.db.models import Q


class BuildResource(ModelResource):
	def apply_filters(self, request, applicable_filters):
		base_list = super(BuildResource, self).apply_filters(request, applicable_filters)

		q_list = None
		all_meta_cats = MetaDataCategory.objects.prefetch_related('values').filter(slug__in = request.GET)
		for meta_cat in all_meta_cats:
			meta_value = request.GET.get(meta_cat.slug, None)
			if meta_value:
				q_subset = 	Q(metadata__category__slug = meta_cat.slug, metadata__value = meta_value)
				
				if q_list is None:
					q_list = base_list.filter(q_subset).distinct()
				else:
					q_list &= base_list.filter(q_subset).distinct()

		if q_list is None:
			return base_list
		else:
			return q_list


	class Meta:
		queryset = Build.objects.all()
		resource_name = 'build'


class MetaDataCategoryResource(ModelResource):
	class Meta:
		queryset = MetaDataCategory.objects.all()
		resource_name = 'metadatacategory'
		filtering = {
			'slug': ALL
		}


class MetaDataResource(ModelResource):
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
