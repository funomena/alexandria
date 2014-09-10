from datastore.models import ArtifactCategory, Artifact
from django.contrib import admin

@admin.register(ArtifactCategory)
class ArtifactCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    pass
