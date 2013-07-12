from django.contrib import admin 
from datastore.models import *


def metadata_display_function(metadata_category):
	def display_function(obj):
		m = obj.metadata.get(category=metadata_category)
		return m.value

	display_function.short_description = metadata_category.friendly_name
	return display_function


class BuildAdmin(admin.ModelAdmin):
	def generate_list_display():
		all_meta_categories = MetaDataCategory.objects.all()
		display = ('name', )
		for cat in all_meta_categories:
			display = display + (metadata_display_function(cat),)
		return display

	list_display = generate_list_display()


admin.site.register(Build, BuildAdmin)
admin.site.register(MetaDataCategory)
admin.site.register(MetaData)
admin.site.register(ExtraDataType)
admin.site.register(ExtraDataValue)
admin.site.register(ArtifactType)
admin.site.register(Artifact)
