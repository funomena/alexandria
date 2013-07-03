from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import utc
import datetime

class MetaDataCategory(models.Model):
	"""
		A category of searchable metadata about builds in this archive.
		Examples include Git Branch, Build Number, Build Configuration, etc.
		Contains an implied field ``values``.
	"""
	slug = models.SlugField(blank=True)
	friendly_name = models.CharField(max_length=64)

	def __unicode__(self):
		return unicode(self.friendly_name)

	def save(self, *args, **kwargs):
		if not self.slug or self.slug == "":
			self.slug = slugify(self.friendly_name)

		return super(MetaDataCategory, self).save(*args, **kwargs)


class MetaData(models.Model):
	"""
		A value of a ``MetaDataCategory`` that applies to one or more ``Builds``.
		Contains an implied field ``builds``.
	"""
	category = models.ForeignKey(MetaDataCategory, related_name='values')
	value = models.CharField(max_length=128)

	def __unicode__(self):
		return u"%s: %s" % (self.category.friendly_name, self.value)


class Build(models.Model):
	"""
		A specific build, which can be sorted and filtered by one or more ``MetaData`` values.
		Contains the implied fields ``extra_data`` and ``artifacts``.
	"""
	name = models.CharField(max_length=128, null=True)
	created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.utcnow().replace(tzinfo=utc))
	metadata = models.ManyToManyField(MetaData, related_name='builds')
	starred = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(self.name)


class ExtraDataType(models.Model):
	""" 
		A type of extra data that is not searchable or used to categorize a build.
		Examples include build logs, associated JIRA tickets, and Github URLs.
		Contains the implied field ``values`` which links to multiple ``ExtraDataValue``s
	"""
	slug = models.SlugField()
	friendly_name = models.CharField(max_length=64)

	def __unicode__(self):
		return unicode(self.friendly_name)

	def save(self, *args, **kwargs):
		if not self.slug or self.slug == "":
			self.slug = slugify(self.friendly_name)

		return super(ExtraDataType, self).save(*args, **kwargs)


class ExtraDataValue(models.Model):
	"""
		A piece of additional data of a specific ``ExtraDataType`` that is not searchable or 
		used to categorize a build.  This contains build data that is not necessary for 
		finding a build, but may be useful after it's found.  Examples include build logs, 
		JIRA tickets, and Github URLs.
	"""
	ed_type = models.ForeignKey(ExtraDataType, related_name='values')
	value = models.TextField()
	build = models.ForeignKey(Build, related_name='extra_data')

	def __unicode__(self):
		return u"%s: %s" % (self.ed_type.friendly_name, self.value)


class ArtifactType(models.Model):
	"""
		A type of build artifact that this build archive supports.  Artifacts may or may not
		be application installers.  Support is offered for 3 types of installers:
			iPhone OTA installers
			Android OTA installers
			Regular old download-and-execute installers
		Any artifact that is not an installer should ahve it's ``installer_type`` set to
		"Not Installer"
		Contains an implied field ``instances``.
	"""
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
		if not self.slug or self.slug == "":
			self.slug = slugify(self.friendly_name)
		return super(ArtifactType, self).save(*args, **kwargs)


class Artifact(models.Model):
	"""
		An artifact of a specific ``ArtifactType``.  The artifact should be able to be downloaded
		from the ``download_url`` provided in this object.
	"""
	a_type = models.ForeignKey(ArtifactType, related_name='instances')
	build = models.ForeignKey(Build, related_name='artifacts')
	download_url = models.CharField(max_length=128)

	def __unicode__(self):
		return u"%s (Build %s)" % (self.a_type.friendly_name, self.build.id)
