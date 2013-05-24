from datastore.models import *
from django.test import TestCase


class BuildTest(TestCase):

	def test_build_unicode_is_build_name(self):
		name = "TestName"
		b = Build.objects.create(name=name)
		self.assertEqual(name, unicode(b))


	def test_metadata_category_unicode_is_name(self):
		name = "TestCategory"
		c = MetaDataCategory.objects.create(friendly_name=name)
		self.assertEqual(name, unicode(c))


	def test_metadata_category_auto_slugify(self):
		name = "Test Category"
		c = MetaDataCategory.objects.create(friendly_name=name)
		self.assertEqual(c.slug, "test-category")


	def test_artifact_type_unicode_is_name(self):
		name = "TestType"
		c = ArtifactType.objects.create(friendly_name=name)
		self.assertEqual(name, unicode(c))


	def test_artifact_type_auto_slugify(self):
		name = "Test Type"
		c = ArtifactType.objects.create(friendly_name=name)
		self.assertEqual(c.slug, "test-type")


	def test_metadata_unicode_contains_build_id(self):
		pass


	def test_metadata_unicode_contains_category_name_and_value(self):
		pass
