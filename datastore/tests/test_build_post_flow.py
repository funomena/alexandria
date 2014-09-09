from django.test import TestCase
from rest_framework.test import APIClient

from datastore.models import MetadataCategory, MetadataValue, Tag
from datastore.models import ArtifactCategory, Artifact, Build

class BuildPostFlowTestCase(TestCase):
    fixtures = ['test_fixtures.json']

    def setUp(self):
        self.client = APIClient()


    def test_posting_complete_build_creates_build_object(self):
        self.assertEquals(Build.objects.all().count(), 1)
        build_data = {'name': 'test', 'tags':["Test Tag"], 'metadata': {'test-string-category': "Test String Value"}}
        self.client.post("/build/", build_data, format="json")
        self.assertEquals(Build.objects.all().count(), 2)


    def test_posting_complete_build_creates_metadata_object(self):
        self.assertEquals(MetadataValue.objects.all().count(), 4)
        build_data = {'name': 'test', 'tags':["Test Tag"], 'metadata': {'test-string-category': "BLAH"}}
        self.client.post("/build/", build_data, format="json")
        self.assertEquals(MetadataValue.objects.all().count(), 5)


    def test_posting_new_tag_creates_new_tag_object(self):
        self.assertEquals(Tag.objects.all().count(), 1)
        build_data = {'name': 'test', 'tags':["Test Tag 2"], 'metadata': {'test-string-category': "Test String Value"}}
        self.client.post("/build/", build_data, format="json")
        self.assertEquals(Tag.objects.all().count(), 2)


    def test_posting_incomplete_build_does_not_create_build(self):
        self.assertEquals(Build.objects.all().count(), 1)
        build_data = {'name': 'test', 'tags':["Test Tag"]}
        self.client.post("/build/", build_data, format="json")
        self.assertEquals(Build.objects.all().count(), 1)


    def test_posting_build_with_missing_metadata_does_not_create_build(self):
        self.assertEquals(Build.objects.all().count(), 1)
        build_data = {'name': 'test', 'tags':["Test Tag"], 'metadata': {'test-int-category': "2"}}
        self.client.post("/build/", build_data, format="json")
        self.assertEquals(Build.objects.all().count(), 1)


    def test_posting_build_without_tags_creates_a_build(self):
        self.assertEquals(Build.objects.all().count(), 1)
        build_data = {'name': 'test', 'metadata': {'test-string-category': "TestTEST"}}
        self.client.post("/build/", build_data, format="json")
        self.assertEquals(Build.objects.all().count(), 2)




