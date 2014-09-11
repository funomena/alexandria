from datastore.models import MetadataCategory, MetadataValue
from django.contrib import admin


@admin.register(MetadataValue)
class MetadataValueAdmin(admin.ModelAdmin):
    pass



@admin.register(MetadataCategory)
class MetadataCategoryAdmin(admin.ModelAdmin):
    class MetadataValueInline(admin.TabularInline):
        model = MetadataValue
        fk_name = "category"
        extra = 1

    prepopulated_fields = {'slug':('friendly_name',)}
    fieldsets = (
                    (
                        None,
                        {'fields':(('friendly_name', 'slug',), ('datatype', 'required',),)},
                    ),
                )
    inlines = [MetadataValueInline,]


