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

class FilterTests(AuthenticatedTestCase):
	fixtures = ['filter_test_data']

	def test_get_all_builds_has_8_builds(self):
		r = self.client.get(self.api_prefix + "build/", data=self.valid_auth_params)
		data = json.loads(r.content)

		self.assertEquals(data['meta']['total_count'], 8)


	def test_filter_by_category_1_is_metadata_11_contains_4_builds(self):
		get_params = self.valid_auth_params
		get_params['category-1'] = 'MetaDataValue11'
		r = self.client.get(self.api_prefix + "build/", data=get_params)
		data = json.loads(r.content)

		self.assertEquals(data['meta']['total_count'], 4)


	def test_filter_by_category_2_is_metadata_21_contains_4_builds(self):
		get_params = self.valid_auth_params
		get_params['category-2'] = 'MetaDataValue21'
		r = self.client.get(self.api_prefix + "build/", data=get_params)
		data = json.loads(r.content)

		self.assertEquals(data['meta']['total_count'], 4)


	def test_filter_by_category_1_is_metadata_11_contains_correct_builds(self):
		get_params = self.valid_auth_params
		get_params['category-1'] = 'MetaDataValue11'
		r = self.client.get(self.api_prefix + "build/", data=get_params)
		data = json.loads(r.content)
		builds = data['objects']
		for build in builds:
			self.assertIn("TestBuild1", build['name'])


	def test_filter_by_category_1_is_metadata_11_and_category_2_is_metadata_21_contains_2_builds(self):
		get_params = self.valid_auth_params
		get_params['category-1'] = 'MetaDataValue11'
		get_params['category-2'] = 'MetaDataValue21'
		r = self.client.get(self.api_prefix + "build/", data=get_params)
		data = json.loads(r.content)

		self.assertEquals(data['meta']['total_count'], 2)


	def test_filter_by_category_1_is_metadata_11_and_category_2_is_metadata_21_and_category_3_is_metadata_32_contains_1_builds(self):
		get_params = self.valid_auth_params
		get_params['category-1'] = 'MetaDataValue11'
		get_params['category-2'] = 'MetaDataValue21'
		get_params['category-3'] = 'MetaDataValue32'
		r = self.client.get(self.api_prefix + "build/", data=get_params)
		data = json.loads(r.content)

		self.assertEquals(data['meta']['total_count'], 1)


	def test_filter_by_category_1_is_metadata_11_and_category_2_is_metadata_21_and_category_3_is_metadata_32_contains_accurate_build(self):
		get_params = self.valid_auth_params
		get_params['category-1'] = 'MetaDataValue11'
		get_params['category-2'] = 'MetaDataValue21'
		get_params['category-3'] = 'MetaDataValue32'
		r = self.client.get(self.api_prefix + "build/", data=get_params)
		data = json.loads(r.content)
		build = data['objects'][0]

		self.assertEquals(build['name'], "TestBuild136")


	def test_metadata_filter_by_category_1_is_metadata_11_contains_5_metadatas(self):
		get_params = self.valid_auth_params
		get_params['category-1'] = 'MetaDataValue11'
		r = self.client.get(self.api_prefix + "metadata/", data=get_params)
		data = json.loads(r.content)

		self.assertEquals(data['meta']['total_count'], 5)
		for obj in data['objects']:
			self.assertNotEquals(obj['id'], 2)


	def test_metadata_filter_by_category_2_is_metadata_21_contains_5_metadatas(self):
		get_params = self.valid_auth_params
		get_params['category-2'] = 'MetaDataValue21'
		r = self.client.get(self.api_prefix + "metadata/", data=get_params)
		data = json.loads(r.content)

		self.assertEquals(data['meta']['total_count'], 5)
		for obj in data['objects']:
			self.assertNotEquals(obj['id'], 4)


	def test_metadata_filter_by_category_1_is_metadata_11_and_category_2_is_metadata_21_contains_4_metadatas(self):
		get_params = self.valid_auth_params
		get_params['category-1'] = 'MetaDataValue11'
		get_params['category-2'] = 'MetaDataValue21'
		r = self.client.get(self.api_prefix + "metadata/", data=get_params)
		data = json.loads(r.content)

		self.assertEquals(data['meta']['total_count'], 4)
		for obj in data['objects']:
			self.assertNotEquals(obj['id'], 2)
			self.assertNotEquals(obj['id'], 4)


	def test_metadata_filter_by_category_1_is_metadata_11_and_category_2_is_metadata_21_and_category_3_is_metadata_32_contains_3_metadatas(self):
		get_params = self.valid_auth_params
		get_params['category-1'] = 'MetaDataValue11'
		get_params['category-2'] = 'MetaDataValue21'
		get_params['category-3'] = 'MetaDataValue32'
		r = self.client.get(self.api_prefix + "metadata/", data=get_params)
		data = json.loads(r.content)

		self.assertEquals(data['meta']['total_count'], 3)
		for obj in data['objects']:
			self.assertNotEquals(obj['id'], 2)
			self.assertNotEquals(obj['id'], 4)
			self.assertNotEquals(obj['id'], 5)

