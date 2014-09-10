from datastore.models import MetadataCategory, MetadataValue
from django.contrib import admin

@admin.register(MetadataCategory)
class MetadataCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(MetadataValue)
class MetadataValueAdmin(admin.ModelAdmin):
    pass
