from datastore.models import *
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseRedirect

class ViewTests(TestCase):
	fixtures = ['filter_test_data']

	def setUp(self):
		super(ViewTests, self).setUp()
		self.user = User.objects.create_user('timmygclef', 'timmygclef@example.com', 'secret')
		self.client = Client()
		self.client.login(username='timmygclef', password='secret')


	def test_index_page_requires_auth(self):
		url = '/'
		self.client.logout()
		r = self.client.get(url)
		self.assertIsInstance(r, HttpResponseRedirect)


	def test_latest_page_returns_page(self):
		url = '/'
		r = self.client.get(url)
		self.assertEquals(r.status_code, 200)


	def test_latest_page_requires_auth(self):
		url = '/latest/'
		self.client.logout()
		r = self.client.get(url)
		self.assertIsInstance(r, HttpResponseRedirect)


	def test_latest_page_returns_page(self):
		url = '/latest/'
		r = self.client.get(url)
		self.assertEquals(r.status_code, 200)


	def test_build_page_requires_auth(self):
		url = '/build/1/'
		self.client.logout()
		r = self.client.get(url)
		self.assertIsInstance(r, HttpResponseRedirect)


	def test_build_page_returns_page(self):
		url = '/build/1/'
		r = self.client.get(url)
		self.assertEquals(r.status_code, 200)


	def test_latest_page_returns_page(self):
		url = '/latest/'
		r = self.client.get(url)
		self.assertEquals(r.status_code, 200)


	def test_filter_page_requires_auth(self):
		url = '/filter/'
		self.client.logout()
		r = self.client.get(url)
		self.assertIsInstance(r, HttpResponseRedirect)


	def test_filter_page_returns_page(self):
		url = '/filter/'
		r = self.client.get(url)
		self.assertEquals(r.status_code, 200)
