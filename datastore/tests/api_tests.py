from datastore.models import *
from tastypie.test import ResourceTestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.http.response import HttpResponseNotFound
from tastypie.models import ApiKey
from tastypie.http import HttpUnauthorized
from datastore.tests.authenticated_tests import AuthenticatedTestCase
import json
import urllib

class APITests(AuthenticatedTestCase):
	fixtures = ['api_test_data']

	def test_api_exists_at_expected_url(self):
		r = self.client.get(self.api_prefix, data={'format':'json'})
		self.assertNotIsInstance(r, HttpResponseNotFound)


	def test_build_api_requires_auth(self):
		r = self.client.get(self.api_prefix + "build/", data={'format':'json'})
		self.assertIsInstance(r, HttpUnauthorized)
		r = self.client.get(self.api_prefix + "build/", data=self.valid_auth_params)
		self.assertNotIsInstance(r, HttpUnauthorized)


	"""
	BUILD API TESTS

	Expected format for single query:

	{
		'name': string,
		'id': int,
		'created': datetime,
		'starred': bool,
		'metadata': [
			{
				'category_name': string,
				'value': string,
				'resource_uri': string			
			}
			...
		]
		'extra_data': [
			{
				'category_name': string,
				'value': string	
			}
			...
		],
		'installers': [
			{
				'type_name': string,
				'download_url': string,
				'resource_uri': string			
			}
			...
		],
		'other_artifacts':[
			{
				'type_name': string,
				'download_url': string,
				'resource_uri': string			
			}
			...
		]
	}

	Expected format for group query:

	{
		'meta': {
			"limit": int,
			"next": ,
			"offset": int,
			"previous": ,
			"total_count": int
		},
		'objects': [
			{
				"created": datetime,
				"id": int,
				"name": string,
				"resource_uri": string,
				"starred": boolean
			}
			...
		]
	}
	"""

	def test_build_get_all_has_meta_section_with_total_count_field(self):
		r = self.client.get(self.api_prefix + "build/", data=self.valid_auth_params)
		data = json.loads(r.content)
		self.assertIn('meta', data)
		self.assertIn('total_count', data['meta'])


	def test_build_get_detail_has_name_id_starred_and_created_field(self):
		r = self.client.get(self.api_prefix + "build/1/", data=self.valid_auth_params)
		data = json.loads(r.content)
		self.assertIn('name', data)
		self.assertIn('id', data)
		self.assertIn('created', data)
		self.assertIn('starred', data)


	def test_build_get_detail_has_valid_metadata_list(self):
		r = self.client.get(self.api_prefix + "build/1/", data=self.valid_auth_params)
		data = json.loads(r.content)

		self.assertIn('metadata', data)
		self.assertEquals(1, len(data['metadata']))

		metadata = data['metadata'][0]
		self.assertIn('category', metadata)
		self.assertIn('value', metadata)
		self.assertIn('resource_uri', metadata)

		self.assertEquals(metadata['category'], "Test Category")


	def test_build_get_detail_has_metadata_with_accurate_resource_uri(self):
		r = self.client.get(self.api_prefix + "build/1/", data=self.valid_auth_params)
		data = json.loads(r.content)

		metadata = data['metadata'][0]
		m = self.client.get(metadata['resource_uri'], data=self.valid_auth_params)
		test_data = json.loads(m.content)

		self.assertEquals(metadata['category'], test_data['category'])
		self.assertEquals(metadata['value'], test_data['value'])


	def test_build_get_detail_has_valid_extra_data_list(self):
		r = self.client.get(self.api_prefix + "build/1/", data=self.valid_auth_params)
		data = json.loads(r.content)

		self.assertIn('extra_data', data)
		self.assertEquals(1, len(data['extra_data']))

		extra_data = data['extra_data'][0]
		self.assertIn('type', extra_data)
		self.assertIn('value', extra_data)
		self.assertNotIn('resource_uri', extra_data)

		self.assertEquals(extra_data['type'], "Test Extra Data")


	def test_build_get_detail_has_valid_installer_list(self):
		r = self.client.get(self.api_prefix + "build/1/", data=self.valid_auth_params)
		data = json.loads(r.content)

		self.assertIn('installers', data)
		self.assertEquals(1, len(data['installers']))

		installer = data['installers'][0]
		self.assertIn('type_name', installer)
		self.assertIn('download_url', installer)
		self.assertIn('resource_uri', installer)

		self.assertEquals(installer['type_name'], "Test Installer")


	def test_build_get_detail_has_valid_other_artifact_list(self):
		r = self.client.get(self.api_prefix + "build/1/", data=self.valid_auth_params)
		data = json.loads(r.content)

		self.assertIn('other_artifacts', data)
		self.assertEquals(1, len(data['other_artifacts']))

		other_artifact = data['other_artifacts'][0]
		self.assertIn('type_name', other_artifact)
		self.assertIn('download_url', other_artifact)
		self.assertIn('resource_uri', other_artifact)

		self.assertEquals(other_artifact['type_name'], "Test Other Artifact")


	def test_post_build_creates_and_returns_build_data(self):
		initial_num_meta_datas = len(MetaData.objects.all())
		post_data = {}
		post_data["metadata"] = [
									{"category": "Test Category", "value": "MetaDataValue2"}
								]
		post_data["extra_data"] = 	[
										{"ed_type": "Test Extra Data", "value": "ExtraData2"}
									]
		p = self.api_client.post(self.api_prefix + "build/", data=post_data, content_type='application/json', authentication=self.api_auth)
		self.assertEquals(p.status_code, 201)
		post_returned_data = json.loads(p.content)
		self.assertIn('id', post_returned_data)
		self.assertEquals(len(post_returned_data['metadata']), 1)

		r = self.client.get(self.api_prefix + "build/" + str(post_returned_data['id']) + "/", data=self.valid_auth_params)
		retrieved_data = json.loads(r.content)
		metadata = retrieved_data['metadata'][0]
		self.assertEquals(metadata['category'], "Test Category")
		self.assertEquals(metadata['value'], "MetaDataValue2")


	def test_post_build_accepts_and_creates_new_metadata(self):
		initial_num_meta_datas = len(MetaData.objects.all())
		post_data = {}
		post_data["metadata"] = [
									{"category": "Test Category", "value": "MetaDataValue2"}
								]
		post_data["extra_data"] = 	[
										{"ed_type": "Test Extra Data", "value": "ExtraData2"}
									]
		p = self.api_client.post(self.api_prefix + "build/", data=post_data, content_type='application/json', authentication=self.api_auth)
		self.assertEquals(p.status_code, 201)

		r = self.client.get(self.api_prefix + "build/", data=self.valid_auth_params)
		data = json.loads(r.content)
		self.assertEquals(data['meta']['total_count'], 2)

		# Test if the post created a new metadata value
		self.assertEquals(len(MetaData.objects.all()), initial_num_meta_datas + 1)

		#Sanity check to see if the API catches the new values
		m = self.client.get(self.api_prefix + "metadata/", data=self.valid_auth_params)
		data = json.loads(m.content)
		self.assertEquals(initial_num_meta_datas + 1, data['meta']['total_count'])


	def test_post_build_accepts_and_uses_existing_metadata(self):
		initial_num_meta_datas = len(MetaData.objects.all())
		post_data = {}
		post_data["metadata"] = [
									{"category": "Test Category", "value": "MetaDataValue1"}
								]
		post_data["extra_data"] = 	[
										{"ed_type": "Test Extra Data", "value": "ExtraData2"}
									]
		p = self.api_client.post(self.api_prefix + "build/", data=post_data, content_type='application/json', authentication=self.api_auth)
		self.assertEquals(p.status_code, 201)

		# Test if the post created a new metadata value
		self.assertEquals(len(MetaData.objects.all()), initial_num_meta_datas)

		#Sanity check to see if the API catches the new values
		m = self.client.get(self.api_prefix + "metadata/", data=self.valid_auth_params)
		data = json.loads(m.content)
		self.assertEquals(initial_num_meta_datas, data['meta']['total_count'])

