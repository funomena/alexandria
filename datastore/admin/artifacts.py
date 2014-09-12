from datastore.models import ArtifactCategory, Artifact
from datastore.admin.forms import artifact, artifact_category
from django.contrib import admin


class ArtifactInline(admin.TabularInline):
    model = Artifact
    extra = 0
    def download(self, obj):
        return '<a class="grp-button" href="/download/%s">Download</a>' % obj.pk

    readonly_fields = ('__str__', 'download', 'file_size', 'md5_hash', 'verified',)
    fields = ('__str__', 'download', 'file_size', 'md5_hash', 'verified',)


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
    def download(self, obj):
        return '<a class="grp-button" href="/download/%s">Download</a>' % obj.pk

    download.short_description = ""

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('__str__', 'download')
        else:
            return ('__str__', 'download', 'file_size', 'md5_hash', 'verified',)


    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return (('__str__', 'download'), 's3_key', ('file_size', 'md5_hash', 'verified', ), )
        else:
            return (('__str__', 'download'), ('file_size', 'md5_hash', 'verified', ), )
