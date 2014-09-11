from datastore.models import ArtifactCategory, Artifact
from datastore.admin.forms import artifact, artifact_category
from django.contrib import admin


class ArtifactInline(admin.StackedInline):
    model = Artifact
    extra = 0 


@admin.register(ArtifactCategory)
class ArtifactCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('friendly_name',)}
    fieldsets = (
                    (
                        None,
                        {'fields':(('friendly_name', 'slug',), ('installer_type', 'extension',),)},
                    ),
                )

    inlines = [ArtifactInline, ]


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    
    pass
