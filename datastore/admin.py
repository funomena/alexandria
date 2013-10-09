from django.contrib import admin 
from django.utils.translation import ugettext_lazy as _
from datastore.models import *
from datetime import date, timedelta


def metadata_display_function(metadata_category):
	def display_function(obj):
		m = obj.metadata.get(category=metadata_category)
		return m.value

	display_function.short_description = metadata_category.friendly_name
	return display_function


class CreatedListFilter(admin.SimpleListFilter):
	title = _('Created')

	parameter_name = 'created'

	def lookups(self, request, model_admin):
		return (
			('today', _('Today')),
			('yesterday', _('Yesterday')),
			('week', _('Past Week')),
			('month', _('Past Month')),
			('-7day', _('Older than a week')),
			('-30day', _('Older than a month')),
		)
	
	def queryset(self, request, queryset):

		today = date.today()
		if self.value() == 'today':
			return queryset.filter(created__startswith=today)
		elif self.value() == 'yesterday':
			return queryset.filter(created__startswith=(today - timedelta(days=1)))
		elif self.value() == 'week':
			return queryset.filter(created__gte=(today - timedelta(days=7)))
		elif self.value() == 'month':
			return queryset.filter(created__gte=(today - timedelta(days=30)))
		elif self.value() == '-7day':
			return queryset.filter(created__lte=(today - timedelta(days=7)))
		elif self.value() == '-30day':
			return queryset.filter(created__lte=(today - timedelta(days=30)))

		return queryset


def metadata_filter_function(metadata_category):
	class MetadataListFilter(admin.SimpleListFilter):
		title = _(metadata_category.friendly_name)

		parameter_name = metadata_category.slug

		def lookups(self, request, model_admin):
			for val in metadata_category.values.all():
				yield (val.value, _(val.value))
		
		def queryset(self, request, queryset):
			try:
				queriedMetadata = MetaData.objects.get(value=self.value(), category=metadata_category)
			except:
				pass
			else:
				return queryset.filter(metadata__in=[queriedMetadata.pk])

	return MetadataListFilter


class BuildAdmin(admin.ModelAdmin):
	def generate_list_display():
		all_meta_categories = MetaDataCategory.objects.all()
		display = ('name', )
		for cat in all_meta_categories:
			display = display + (metadata_display_function(cat),)
		return display

	def generate_list_filter():
		all_meta_categories = MetaDataCategory.objects.all()
		l_filter = (CreatedListFilter,)
		for cat in all_meta_categories:
			l_filter = l_filter + (metadata_filter_function(cat),)
		return l_filter

	list_display = generate_list_display()
	list_filter = generate_list_filter()


admin.site.register(Build, BuildAdmin)
admin.site.register(MetaDataCategory)
admin.site.register(MetaData)
admin.site.register(ExtraDataType)
admin.site.register(ExtraDataValue)
admin.site.register(ArtifactType)
admin.site.register(Artifact)
