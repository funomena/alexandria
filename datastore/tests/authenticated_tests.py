from datastore.models import *
from tastypie.test import ResourceTestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.http.response import HttpResponseNotFound
from tastypie.models import ApiKey
from tastypie.http import HttpUnauthorized
import json
import urllib

class AuthenticatedTestCase(ResourceTestCase):

	def setUp(self):
		super(AuthenticatedTestCase, self).setUp()
		self.user = User.objects.create_user('timmygclef', 'timmygclef@example.com', 'secret')
		self.client = Client()
		self.api_key = ApiKey.objects.create(user=self.user)
		self.api_prefix = "/api/v0/"
		self.valid_auth_params = {'format':'json', 'username': self.user.username, 'api_key':self.api_key.key}
		self.api_auth = self.create_apikey(self.user.username, self.api_key.key)
