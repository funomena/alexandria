from django.test import TestCase
from unittest import expectedFailure

from datastore.models import MetadataCategory, MetadataValue, Tag
from datastore.models import ArtifactCategory, Artifact, Build

from datastore.serializers import   MetadataCategorySerializer,\
                                    MetadataValueSerializer,\
                                    TagSerializer,\
                                    ArtifactCategorySerializer,\
                                    ArtifactSerializer,\
                                    BuildSerializer

from rest_framework.test import APIRequestFactory


class SeralizerTestCase(TestCase):
    fixtures = ['test_fixtures.json']

    def setUp(self):
        factory = APIRequestFactory()
        self.fake_req = factory.get('')


    def test_metadata_category_serializer_contains_correct_fields(self):
        serializer = MetadataCategorySerializer(MetadataCategory.objects.get(pk=1),
                                                context={'request': self.fake_req})
        self.assertIn("slug", serializer.data)
        self.assertIn("friendly_name", serializer.data)
        self.assertIn("required", serializer.data)
        self.assertIn("values", serializer.data)


    def test_metadata_category_serializer_returns_list_of_value_ids(self):
        serializer = MetadataCategorySerializer(MetadataCategory.objects.get(pk=1),
                                                context={'request': self.fake_req})
        self.assertIn("values", serializer.data)
        self.assertIsInstance(serializer.data['values'], list)
        self.assertIsInstance(serializer.data['values'][0], int)


    def test_metadata_value_serializer_returns_correct_fields(self):
        serializer = MetadataValueSerializer(   MetadataValue.objects.get(pk=1),
                                                context={'request': self.fake_req})
        self.assertIn("category", serializer.data)
        self.assertIn("value", serializer.data)


    def test_metadata_value_serializer_returns_serialized_metadata_category(self):
        serializer = MetadataValueSerializer(   MetadataValue.objects.get(pk=1),
                                                context={'request': self.fake_req})
        self.assertIn("category", serializer.data)
        self.assertIsInstance(serializer.data['category'], unicode)


    def test_metadata_value_serializer_returns_list_of_build_ids(self):
        serializer = MetadataValueSerializer(   MetadataValue.objects.get(pk=1),
                                                context={'request': self.fake_req})
        self.assertIn("builds", serializer.data)
        self.assertIsInstance(serializer.data['builds'], list)
        self.assertIsInstance(serializer.data['builds'][0], int)


    def test_tag_serializer_returns_correct_fields(self):
        serializer = TagSerializer( Tag.objects.get(pk=1),
                                    context={'request': self.fake_req})
        self.assertIn("value", serializer.data)
        self.assertIn("builds", serializer.data)


    def test_tag_serialzer_returns_list_of_build_pks(self):
        serializer = TagSerializer( Tag.objects.get(pk=1),
                                    context={'request': self.fake_req})
        self.assertIn("builds", serializer.data)
        self.assertIsInstance(serializer.data['builds'], list)
        self.assertIsInstance(serializer.data['builds'][0], int)


    def test_build_serializer_returns_correct_fields(self):
        serializer = BuildSerializer(   Build.objects.get(pk=1),
                                        context={'request': self.fake_req})
        self.assertIn("name", serializer.data)
        self.assertIn("metadata", serializer.data)
        self.assertIn("tags", serializer.data)
        self.assertIn("artifacts", serializer.data)


    def test_build_serializer_returns_full_list_of_tags(self):
        serializer = BuildSerializer(   Build.objects.get(pk=1),
                                        context={'request': self.fake_req})
        self.assertIn("tags", serializer.data)
        self.assertIsInstance(serializer.data['tags'], list)
        self.assertIsInstance(serializer.data['tags'][0], unicode)

    def test_build_serializer_returns_list_of_metadata(self):
        serializer = BuildSerializer(   Build.objects.get(pk=1),
                                        context={'request': self.fake_req})
        self.assertIn("metadata", serializer.data)
        self.assertIsInstance(serializer.data['metadata'], list)
        self.assertIsInstance(serializer.data['metadata'][0], dict)
	self.assertIn("value", serializer.data['metadata'][0])
	self.assertIn("category", serializer.data['metadata'][0])


    def test_build_serializer_returns_list_of_artifact_pks(self):
        serializer = BuildSerializer(   Build.objects.get(pk=1),
                                        context={'request': self.fake_req})
        self.assertIn("artifacts", serializer.data)
        self.assertIsInstance(serializer.data['artifacts'], list)
        self.assertIsInstance(serializer.data['artifacts'][0], int)


