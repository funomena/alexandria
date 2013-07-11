from datastore.models import *
from tastypie.test import ResourceTestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from tastypie.models import ApiKey
from tastypie.http import HttpUnauthorized
from datastore.tests.authenticated_tests import AuthenticatedTestCase
from datastore.uploads import post_artifact_to_s3
from django.conf import settings
import json
import urllib
import boto
import requests
import os

class UploadTests(AuthenticatedTestCase):
	fixtures = ['api_test_data']

	def setUp(self):
		super(UploadTests, self).setUp()
		self.test_payload_content = "Though this be madness, yet there is method in't."
		self.test_payload = open("payload", 'w')
		self.test_payload.write(self.test_payload_content)
		self.test_payload.close()
		self.s3 = boto.connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_ACCESS_SECRET)
		self.bucket = self.s3.lookup(settings.S3_BUCKET)

	def tearDown(self):
		keys = self.bucket.get_all_keys()
		key_names = map(lambda x: x.name, keys)
		self.bucket.delete_keys(key_names)
		os.remove(self.test_payload.name)


	def test_download_urls_redirect_to_publicly_uploaded_files(self):
		self.client.login(username=self.user.username, password=self.raw_password)
		r = self.client.get("/download/1/")
		self.assertIsInstance(r, HttpResponseRedirect)
		self.assertEquals(r['Location'], "http://download.com/1")


	def test_post_to_s3_task_posts_file_contents_and_updates_artifact(self):
		created_artifact = Artifact.objects.create(a_type_id=1, build_id=1, is_secure=True)
		created_artifact_id = created_artifact.pk
		post_artifact_to_s3(created_artifact_id, self.test_payload_content)

		updated_artifact = Artifact.objects.get(pk=created_artifact_id)
		self.assertNotEquals(updated_artifact.secure_uuid, None)

		key = self.bucket.lookup(updated_artifact.secure_uuid)
		key_contents = key.get_contents_as_string()
		self.assertEquals(self.test_payload_content, key_contents)


	def test_uploading_artifacts_requires_auth(self):
		upload_data = {'build_id': 1, 'type': 'Test Installer'}
		files = {'payload': open(self.test_payload.name, 'rb')}
		p = self.api_client.post("/upload/", data=upload_data, files=files, content_type='application/json')
		self.assertEquals(p.status_code, 401)


	def test_uploading_artifacts_returns_pointer_to_valid_artifact(self):
		upload_data = {'build_id': 1, 'type': 'Test Installer'}
		files = {'payload': open(self.test_payload.name, 'rb')}
		p = self.api_client.post("/upload/", data=upload_data, authentication=self.api_auth, files=files, content_type='application/json')
		self.assertEquals(p.status_code, 201)
		artifact_pointer = json.loads(p.content)

		created_artifact = Artifact.objects.get(pk=artifact_pointer['id'])
		self.assertNotEquals(created_artifact, None)
		self.assertNotEquals(created_artifact.secure_uuid, None)

		# Validate the posted file too
		key = self.bucket.lookup(created_artifact.secure_uuid)
		key_contents = key.get_contents_as_string()
		self.assertEquals(self.test_payload_content, key_contents)


	def test_uploading_artifacts_and_accessing_returns_s3_download_link(self):
		upload_data = {'build_id': 1, 'type': 'Test Installer'}
		files = {'payload': open(self.test_payload.name, 'rb')}
		p = self.api_client.post("/upload/", data=upload_data, authentication=self.api_auth, files=files, content_type='application/json')
		self.assertEquals(p.status_code, 201)
		artifact_pointer = json.loads(p.content)

		self.client.login(username=self.user.username, password=self.raw_password)
		r = self.client.get("/download/%s/" % artifact_pointer['id'])
		self.assertIsInstance(r, HttpResponseRedirect)
		self.assertNotIn(r['Location'], "download.com")
		artifact_dl = requests.get(r['Location'])
		self.assertEquals(artifact_dl.text, self.test_payload_content)
		self.assertIn("filename=test-installer_1.test", artifact_dl.headers["Content-Disposition"])


	def test_post_artifact_with_public_url(self):
		artifact_data = {'type': 'Test Installer', 'build': 1, 'public_url':'http://download.com/test'}
		p = self.api_client.post(self.api_prefix + "artifact/", data=artifact_data, content_type='application/json', authentication=self.api_auth)
		self.assertEquals(p.status_code, 201)
		returned_data = json.loads(p.content)
		self.assertIn('download_url', returned_data)
		self.assertNotIn('public_url', returned_data)

