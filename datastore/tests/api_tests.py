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

	def setUp(self):
		super(APITests, self).setUp()
		self.build_data_with_all_new_meta = {
			"metadata": [
							{"category": "Test Category", "value": "MetaDataValue2"},
							{"category": "Test Category 2", "value": "OtherMetaDataValue2"}
						],
			"extra_data":	[
								{"ed_type": "Test Extra Data", "value": "ExtraData2"}
							]
		}
		self.build_data_with_some_new_meta = {
			"metadata": [
							{"category": "Test Category", "value": "MetaDataValue2"},
							{"category": "Test Category 2", "value": "OtherMetaDataValue1"}
						],
			"extra_data":	[
								{"ed_type": "Test Extra Data", "value": "ExtraData2"}
							]
		}
		self.build_data_with_no_new_meta = {
			"metadata": [
							{"category": "Test Category", "value": "MetaDataValue1"},
							{"category": "Test Category 2", "value": "OtherMetaDataValue1"}
						],
			"extra_data":	[
								{"ed_type": "Test Extra Data", "value": "ExtraData2"}
							]
		}

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
		'other_artifacts':[
			{
				'type': string,
				'download_url': string,
				'resource_uri': string,
				'installer_type': string			
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
		self.assertEquals(2, len(data['metadata']))

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
		self.assertIn('ed_type', extra_data)
		self.assertIn('value', extra_data)
		self.assertNotIn('resource_uri', extra_data)

		self.assertEquals(extra_data['ed_type'], "Test Extra Data")


	def test_build_get_detail_has_valid_artifact_list(self):
		r = self.client.get(self.api_prefix + "build/1/", data=self.valid_auth_params)
		data = json.loads(r.content)

		self.assertIn('artifacts', data)
		self.assertEquals(2, len(data['artifacts']))

		installer = data['artifacts'][0]
		self.assertIn('a_type', installer)
		self.assertIn('download_url', installer)
		self.assertIn('resource_uri', installer)


	def test_post_build_accepts_and_creates_new_metadata(self):
		# Make sure we create 2 new metadata objects on the backend
		initial_num_meta_datas = len(MetaData.objects.all())

		p = self.api_client.post(self.api_prefix + "build/", data=self.build_data_with_all_new_meta, content_type='application/json', authentication=self.api_auth)
		self.assertEquals(p.status_code, 201)

		r = self.client.get(self.api_prefix + "build/", data=self.valid_auth_params)
		data = json.loads(r.content)

		# Make sure we made a build
		self.assertEquals(data['meta']['total_count'], 2)

		# Test if the post created a new metadata value
		self.assertEquals(len(MetaData.objects.all()), initial_num_meta_datas + 2)

		#Sanity check to see if the API catches the new values
		m = self.client.get(self.api_prefix + "metadata/", data=self.valid_auth_params)
		data = json.loads(m.content)
		self.assertEquals(initial_num_meta_datas + 2, data['meta']['total_count'])


	def test_post_build_accepts_and_uses_existing_metadata(self):
		# Make sure we don't create any new metadata on the backend
		initial_num_meta_datas = len(MetaData.objects.all())

		p = self.api_client.post(self.api_prefix + "build/", data=self.build_data_with_no_new_meta, content_type='application/json', authentication=self.api_auth)
		self.assertEquals(p.status_code, 201)

		# Test if the post created a new metadata value
		self.assertEquals(len(MetaData.objects.all()), initial_num_meta_datas)

		#Sanity check to see if the API catches the new values
		m = self.client.get(self.api_prefix + "metadata/", data=self.valid_auth_params)
		data = json.loads(m.content)
		self.assertEquals(initial_num_meta_datas, data['meta']['total_count'])


	def test_post_build_creates_and_returns_build_data(self):

		p = self.api_client.post(self.api_prefix + "build/", data=self.build_data_with_some_new_meta, content_type='application/json', authentication=self.api_auth)
		self.assertEquals(p.status_code, 201)
		post_returned_data = json.loads(p.content)

		# Make sure the returned build contains an id
		self.assertIn('id', post_returned_data)
		# Make sure the metadata got associated correctly
		self.assertEquals(len(post_returned_data['metadata']), 2)

		# Make sure the returned id is correct
		r = self.client.get(self.api_prefix + "build/" + str(post_returned_data['id']) + "/", data=self.valid_auth_params)
		retrieved_data = json.loads(r.content)
		metadata = retrieved_data['metadata'][1]
		self.assertEquals(metadata['category'], "Test Category")
		self.assertEquals(metadata['value'], "MetaDataValue2")


	def test_build_can_be_starred_with_PATCH_request(self):
		# Sanity check that the build starts out not starred
		r = self.client.get(self.api_prefix + "build/1/", data=self.valid_auth_params)
		data = json.loads(r.content)
		self.assertEquals(data['starred'], False)

		# Patch and test
		p = self.api_client.patch(self.api_prefix + "build/1/", data={'starred': True}, content_type='application/json', authentication=self.api_auth)
		r = self.client.get(self.api_prefix + "build/1/", data=self.valid_auth_params)
		data = json.loads(r.content)
		self.assertEquals(data['starred'], True)


	def test_created_metadatas_have_correct_builds(self):
		p = self.api_client.post(self.api_prefix + "build/", data=self.build_data_with_some_new_meta, content_type='application/json', authentication=self.api_auth)
		p = self.api_client.post(self.api_prefix + "build/", data=self.build_data_with_all_new_meta, content_type='application/json', authentication=self.api_auth)

		# There should be 2 builds with MetaDataValue2
		r = self.api_client.get(self.api_prefix + "metadata/test-category/MetaDataValue2/", data=self.valid_auth_params)
		data = json.loads(r.content)
		self.assertEquals(len(data['builds']), 2)


	def test_updated_metadatas_have_correct_builds(self):
		p = self.api_client.post(self.api_prefix + "build/", data=self.build_data_with_some_new_meta, content_type='application/json', authentication=self.api_auth)
		p = self.api_client.post(self.api_prefix + "build/", data=self.build_data_with_no_new_meta, content_type='application/json', authentication=self.api_auth)

		# There should be 3 builds with MetaDataValue1
		r = self.api_client.get(self.api_prefix + "metadata/test-category-2/OtherMetaDataValue1/", data=self.valid_auth_params)
		data = json.loads(r.content)
		self.assertEquals(len(data['builds']), 3)

