from django.db import models
from django.template.defaultfilters import slugify


class Build(models.Model):
	name = models.CharField(max_length=128)
	created = models.DateTimeField(auto_now_add=True, default="1970-01-01 00:01")
	starred = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name


class MetaDataCategory(models.Model):
	slug = models.SlugField()
	friendly_name = models.CharField(max_length=64)
	is_extra_data = models.BooleanField()

	def __unicode__(self):
		return unicode(self.friendly_name)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.friendly_name)

		return super(MetaDataCategory, self).save(*args, **kwargs)


class MetaData(models.Model):
	category = models.ForeignKey(MetaDataCategory, related_name='values')
	build = models.ForeignKey(Build, related_name='metadata')
	value = models.CharField(max_length=128)

	def __unicode__(self):
		return u"%s: %s (Build %s)" % (self.category.friendly_name, self.value, self.build.id)


class ArtifactType(models.Model):
	INSTALLER_TYPE_NONE = "NOT INSTALLER"
	INSTALLER_TYPE_NORMAL = "NORMAL INSTALLER"
	INSTALLER_TYPE_IPHONE = "IPHONE INSTALLER"
	INSTALLER_TYPE_ANDROID = "ANDROID INSTALLER"

	INSTALLER_TYPES = (
		(INSTALLER_TYPE_NONE, 'Not Installer'),
		(INSTALLER_TYPE_NORMAL, 'Normal Installer'),
		(INSTALLER_TYPE_IPHONE, 'iPhone Installer'),
		(INSTALLER_TYPE_ANDROID, 'Android Installer'),
		)

	slug = models.SlugField()
	friendly_name = models.CharField(max_length=64)
	installer_type = models.CharField(max_length=32, choices=INSTALLER_TYPES, default=INSTALLER_TYPE_NONE)
	extension = models.CharField(max_length=16)

	def __unicode__(self):
		return unicode(self.friendly_name)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.friendly_name)

		return super(ArtifactType, self).save(*args, **kwargs)


class Artifact(models.Model):
	a_type = models.ForeignKey(ArtifactType, related_name='instances')
	build = models.ForeignKey(Build, related_name='artifacts')
	download_url = models.CharField(max_length=128)

	def __unicode__(self):
		return u"%s (Build %s)" % (self.a_type.friendly_name, self.build.id)
