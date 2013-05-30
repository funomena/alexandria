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

class EmuBabyResource(ModelResource):
	def determine_format(self, request):
		return 'application/json'


class MetaDataCategoryResource(EmuBabyResource):
	class Meta:
		queryset = MetaDataCategory.objects.all()
		resource_name = 'metadatacategory'
		filtering = {
			'slug': ALL
		}
		authorization = Authorization()
		authentication = ApiKeyAuthentication()


class MetaDataResource(EmuBabyResource):

	category = fields.ForeignKey(MetaDataCategoryResource, 'category', full=True, full_detail=True)

	builds = fields.ToManyField('datastore.api.BuildResource', 'builds', related_name='metadata', blank=True, null=True)


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


	def dehydrate(self, bundle):
		builds = []
		for b in Build.objects.filter(metadata__id=bundle.obj.id):
			builds.append(b.id)
		dehydrated_data = {'value': bundle.obj.value, 'category': bundle.obj.category.friendly_name, 'slug':bundle.obj.category.slug, 'builds': builds, 'resource_uri': self.get_resource_uri(bundle)}
		return dehydrated_data


	def hydrate(self, bundle):
		cat, created = MetaDataCategory.objects.get_or_create(friendly_name=bundle.data["category"])
		bundle.data["category"] = cat
		return bundle


	class Meta:
		queryset = MetaData.objects.all()
		resource_name = 'metadata'
		filtering = {
			'category': ALL_WITH_RELATIONS
		}
		
		authorization = Authorization()
		authentication = ApiKeyAuthentication()


class ExtraDataTypeResource(EmuBabyResource):
	class Meta:
		queryset = ExtraDataType.objects.all()
		resource_name = 'extradatatype'
		filtering = {
			'slug': ALL
		}
		authorization = Authorization()
		authentication = ApiKeyAuthentication()


class ExtraDataValueResource(EmuBabyResource):

	ed_type = fields.ForeignKey(ExtraDataTypeResource, 'ed_type', full=True, full_detail=True)

	build = fields.ToOneField('datastore.api.BuildResource', 'build')

	def dehydrate(self, bundle):
		dehydrated_data = {'value': bundle.obj.value, 'type': bundle.obj.ed_type.friendly_name}
		return dehydrated_data

	def hydrate(self, bundle):
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
		
		authorization = Authorization()
		authentication = ApiKeyAuthentication()


class BuildResource(EmuBabyResource):
	metadata = fields.ToManyField(MetaDataResource, 'metadata', related_name='builds', use_in='detail', full=True, full_detail=True)

	extra_data = fields.ToManyField(ExtraDataValueResource, 'extra_data', related_name='build', null=True, blank=True, use_in='detail', full=True, full_detail=True)

	installers = fields.ToManyField('datastore.api.ArtifactResource', 
									attribute=lambda bundle: Artifact.objects.filter(build__id=bundle.obj.id).exclude(a_type__installer_type=ArtifactType.INSTALLER_TYPE_NONE),
									null=True,
									blank=True,
									use_in='detail',
									full=True,
									full_detail=True)

	other_artifacts = fields.ToManyField('datastore.api.ArtifactResource', 
										attribute=lambda bundle: Artifact.objects.filter(build__id=bundle.obj.id, 
																						a_type__installer_type=ArtifactType.INSTALLER_TYPE_NONE), 
										null=True,
										blank=True,
										use_in='detail',
										full=True,
										full_detail=True)

	name = fields.CharField(blank=True, null=True, attribute='name')


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
		
		authorization = Authorization()
		authentication = ApiKeyAuthentication()
		always_return_data = True


class ArtifactTypeResource(EmuBabyResource):
	class Meta:
		queryset = ArtifactType.objects.all()
		resource_name = 'artifacttype'
		
		authorization = Authorization()
		authentication = ApiKeyAuthentication()
		filtering = {
			'installer_type': ALL
		}


class ArtifactResource(EmuBabyResource):
	a_type = fields.ForeignKey(ArtifactTypeResource, 'a_type', full=True, full_detail=True)


	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/(?P<a_type__slug>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="a_type_slug_dispatch_detail"),
		]


	def dehydrate(self, bundle):
		dehydrated_data = {'type_name': bundle.data['a_type'].data['friendly_name'], 'download_url': bundle.data['download_url'], 'resource_uri': bundle.data['resource_uri']}
		return dehydrated_data
		

	class Meta:
		queryset = Artifact.objects.all()
		resource_name = 'artifact'
		filtering = {
			'a_type': ALL_WITH_RELATIONS
		}
		
		authorization = Authorization()
		authentication = ApiKeyAuthentication()
