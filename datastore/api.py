from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie import fields, http
from datastore.models import *
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.conf.urls import patterns, include, url
from django.template.defaultfilters import slugify
from datastore.utils import get_build_query_set
import json

class AlexandriaResource(ModelResource):
	def determine_format(self, request):
		return 'application/json'

	def full_dehydrate(self, bundle, for_list=False):
		"""
			A hacky implementation of https://github.com/toastdriven/django-tastypie/pull/615,
			which fixes this issue: https://github.com/toastdriven/django-tastypie/issues/654
		"""
		bundle.data = {}

		return super(AlexandriaResource, self).full_dehydrate(bundle, for_list)


class MetaDataCategoryResource(AlexandriaResource):
	class Meta:
		queryset = MetaDataCategory.objects.all()
		resource_name = 'metadatacategory'
		filtering = {
			'slug': ALL
		}
		authorization = Authorization()
		authentication = ApiKeyAuthentication()


class MetaDataResource(AlexandriaResource):

	category = fields.ForeignKey(MetaDataCategoryResource, 'category', full=True, full_detail=True)

	builds = fields.ToManyField('datastore.api.BuildResource', 'builds', related_name='metadata', blank=True, null=True)

	slug = fields.CharField()


	def apply_filters(self, request, applicable_filters):
		base_list = super(MetaDataResource, self).apply_filters(request, applicable_filters)

		q_list = get_build_query_set(request.GET, Build.objects.all())

		if q_list is None:
			return base_list
		else:
			metadata_ids = []
			for build in q_list:
				for meta in build.metadata.all():
					if not meta.pk in metadata_ids:
						metadata_ids.append(meta.pk)
			return MetaData.objects.filter(pk__in=metadata_ids)


	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/(?P<category__slug>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="meta_category_slug_dispatch_detail"),
			url(r"^(?P<resource_name>%s)/(?P<category__slug>[\w\d_.-]+)/(?P<value>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="meta_category_slug_dispatch_detail"),
		]


	def get_resource_uri(self, bundle_or_obj=None, name='api_dispatch_list'):
		url = super(MetaDataResource, self).get_resource_uri()
		if bundle_or_obj is None:
			return url

		if bundle_or_obj.obj is not None:
			val = bundle_or_obj.obj.value
			slug = bundle_or_obj.obj.category.slug
		else:
			val = bundle_or_obj.data['value']
			slug = bundle_or_obj.data['slug']
		return "%s%s/%s/" % (url, slug, val)


	def dehydrate_builds(self, bundle):
		builds = []
		for b in Build.objects.filter(metadata__id=bundle.obj.id):
			builds.append(b.id)
		return builds


	# Not needed, but here for clarity
	def hydrate_builds(self, bundle):
		bundle.data['builds'] = Build.objects.filter(metadata__id=bundle.obj.id)
		return bundle


	def dehydrate_category(self, bundle):
		return bundle.obj.category.friendly_name


	def hydrate_category(self, bundle):
		cat = MetaDataCategory.objects.get(friendly_name=bundle.data["category"])
		bundle.data['category'] = cat
		return bundle


	def dehydrate_slug(self, bundle):
		return bundle.obj.category.slug


	# Not needed, but here for clarity
	def hydrate_slug(self, bundle):
		return bundle


	class Meta:
		queryset = MetaData.objects.all()
		resource_name = 'metadata'
		filtering = {
			'category': ALL_WITH_RELATIONS
		}
		
		authorization = Authorization()
		authentication = ApiKeyAuthentication()


class ExtraDataTypeResource(AlexandriaResource):
	class Meta:
		queryset = ExtraDataType.objects.all()
		resource_name = 'extradatatype'
		filtering = {
			'slug': ALL
		}
		authorization = Authorization()
		authentication = ApiKeyAuthentication()


class ExtraDataValueResource(AlexandriaResource):

	ed_type = fields.ForeignKey(ExtraDataTypeResource, 'ed_type', full=True, full_detail=True)

	build = fields.ToOneField('datastore.api.BuildResource', 'build')


	def dehydrate_ed_type(self, bundle):
		return bundle.obj.ed_type.friendly_name


	def hydrate_ed_type(self, bundle):
		ed_type = ExtraDataType.objects.get(friendly_name=bundle.data['ed_type'])
		bundle.data['ed_type'] = ed_type
		return bundle


	class Meta:
		queryset = ExtraDataValue.objects.all()
		resource_name = 'extradata'
		filtering = {
			'ed_type': ALL_WITH_RELATIONS,
			'build': ALL_WITH_RELATIONS
		}
		include_resource_uri = False
		
		authorization = Authorization()
		authentication = ApiKeyAuthentication()


class BuildResource(AlexandriaResource):
	metadata = fields.ToManyField(MetaDataResource, 'metadata', related_name='builds', use_in='detail', full=True, full_detail=True)

	extra_data = fields.ToManyField(ExtraDataValueResource, 'extra_data', related_name='build', null=True, blank=True, use_in='detail', full=True, full_detail=True)

	artifacts = fields.ToManyField('datastore.api.ArtifactResource', 'artifacts', null=True, blank=True, use_in='detail', full=True, full_detail=True)

	name = fields.CharField(blank=True, null=True, attribute='name')


	def apply_filters(self, request, applicable_filters):
		base_list = super(BuildResource, self).apply_filters(request, applicable_filters)

		q_list = get_build_query_set(request.GET, base_list)

		if q_list is None:
			return base_list
		else:
			return q_list


	"""
		Kind of hacky, but tastypie was overwriting the m2m relationships on obj_create.
		This persists any existing relationships on save.
	"""
	def obj_create(self, bundle, **kwargs):
		saved_metas = MetaData.objects.all()
		meta_ids_to_build_ids = {}
		for m in saved_metas:
			meta_ids_to_build_ids[m.pk] = map(lambda x: int(x.pk), m.builds.all())
		bundle = super(BuildResource, self).obj_create(bundle, **kwargs)
		for m in MetaData.objects.all():
			if m.pk in meta_ids_to_build_ids:
				ids = meta_ids_to_build_ids[m.pk]
				m.builds.add(*ids)
				m.save()
		return bundle


	class Meta:
		queryset = Build.objects.all()
		resource_name = 'build'
		
		authorization = Authorization()
		authentication = ApiKeyAuthentication()
		always_return_data = True
		allowed_methods = ['get', 'post', 'patch']


class ArtifactTypeResource(AlexandriaResource):
	class Meta:
		queryset = ArtifactType.objects.all()
		resource_name = 'artifacttype'
		
		authorization = Authorization()
		authentication = ApiKeyAuthentication()
		filtering = {
			'installer_type': ALL,
			'slug': ALL
		}


class ArtifactResource(AlexandriaResource):
	a_type = fields.ForeignKey(ArtifactTypeResource, 'a_type', full=True, full_detail=True)

	build = fields.ToOneField(BuildResource, 'build')

	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/(?P<a_type__slug>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="a_type_slug_dispatch_list"),
			url(r"^(?P<resource_name>%s)/(?P<a_type__slug>[\w\d_.-]+)/(?P<id>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="a_type_slug_dispatch_detail"),
		]


	def dehydrate(self, bundle):
		bundle.data['download_url'] = bundle.obj.download_url
		return bundle


	def dehydrate_a_type(self, bundle):
		return bundle.obj.a_type.friendly_name


	def hydrate_a_type(self, bundle):
		a_type = ArtifactType.objects.get(friendly_name=bundle.data['type'])
		bundle.data['a_type'] = a_type
		return bundle


	def dehydrate_build(self, bundle):
		return bundle.obj.build.id


	def hydrate_build(self, bundle):
		b = Build.objects.get(id = bundle.data['build'])
		bundle.data['build'] = b
		return bundle


	class Meta:
		queryset = Artifact.objects.all()
		resource_name = 'artifact'
		filtering = {
			'a_type': ALL_WITH_RELATIONS,
			'build': ALL_WITH_RELATIONS
		}
		fields = ['download_url', 'a_type', 'build', 'secure_uuid']
		excludes = ['public_url']
		always_return_data = True

		authorization = Authorization()
		authentication = ApiKeyAuthentication()
