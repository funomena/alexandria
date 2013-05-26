from datastore.models import *
from django.test import TestCase


class BuildTest(TestCase):
	fixtures = ['test_data']

	def test_build_unicode_is_build_name(self):
		name = "TestName"
		b = Build.objects.create(name=name)
		self.assertEqual(name, unicode(b))


	def test_metadata_category_unicode_is_name(self):
		c = MetaDataCategory.objects.get(pk=1)
		self.assertEqual("Test Category", unicode(c))


	def test_metadata_category_auto_slugify(self):
		c = MetaDataCategory.objects.get(pk=1)
		c.save()
		self.assertEqual(c.slug, "test-category")


	def test_artifact_type_unicode_is_name(self):
		t = ArtifactType.objects.get(pk=1)
		self.assertEqual("Test Type", unicode(t))


	def test_artifact_type_auto_slugify(self):
		t = ArtifactType.objects.get(pk=1)
		t.save()
		self.assertEqual(t.slug, "test-type")


	def test_metadata_unicode_contains_build_id(self):
		m = MetaData.objects.get(pk=1)
		self.assertIn("Build 1", unicode(m))


	def test_metadata_unicode_contains_category_name_and_value(self):
		m = MetaData.objects.get(pk=1)
		self.assertIn("MetaDataValue1", unicode(m))
		self.assertIn("Test Category", unicode(m))


	def test_artifact_unicode_contains_build_id(self):
		a = Artifact.objects.get(pk=1)
		self.assertIn("Build 1", unicode(a))


	def test_artifact_unicode_contains_type_name(self):
		a = Artifact.objects.get(pk=1)
		self.assertIn("Test Type", unicode(a))
