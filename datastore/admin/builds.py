from datastore.models import Build, MetadataCategory, Tag
from django.contrib import admin
from django import forms
from datastore.admin.forms.build_form import BuildForm
from datastore.admin.artifacts import ArtifactInline


def get_valid_artifact_count(build):
    return build.artifacts.filter(verified=True).count()

get_valid_artifact_count.short_description = "Artifact Count"


def meta_display_function(category):
    def display_function(build):
        m = build.metadata.get(category=category)
        return m.value

    display_function.short_description = category.friendly_name
    return display_function


def tag_display_function(tag):
    def display_function(build):
        return build.tags.filter(pk=tag.pk).exists()

    display_function.boolean = True
    display_function.short_description = tag.value
    return display_function


def generate_tag_filter(tag):
    class TagListFilter(admin.SimpleListFilter):
        title = tag.value
        parameter_name = tag.value

        def lookups(self, request, model_admin):
            return (
                ("yes", "yes"),
                ("no", "no"),
            )

        def queryset(self, request, queryset):
            if self.value() == "yes":
                return queryset.filter(tags__id__contains=tag.id)
            elif self.value() == "no":
                return queryset.exclude(tags__id__contains=tag.id)
            else:
                return queryset

    return TagListFilter


def generate_metadata_filter(metadata_category):
    class MetadataListFilter(admin.SimpleListFilter):
        title = metadata_category.friendly_name
        parameter_name = metadata_category.slug
        def lookups(self, request, model_admin):
            for val in metadata_category.values.all():
                yield (val.value, val.value)
        def queryset(self, request, queryset):
            try:
               queriedMetadata = MetaData.objects.get(value=self.value(),category=metadata_category)
            except:
                pass
            else:
                return queryset.filter(metadata__in=[queriedMetadata.pk])
    return MetadataListFilter


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        all_meta_categories = MetadataCategory.objects.all()
        display = ('name', get_valid_artifact_count, )
        for cat in all_meta_categories:
            display = display + (meta_display_function(cat), )
        for tag in Tag.objects.all():
            display = display + (tag_display_function(tag), )
        return display

    def get_list_filter(self, request):
        all_meta_categories = MetadataCategory.objects.all()
        l_filter = ('name', )
        for cat in all_meta_categories:
            l_filter = l_filter + (generate_metadata_filter(cat), )
        all_tags = Tag.objects.all()
        for tag in all_tags:
            l_filter = l_filter + (generate_tag_filter(tag), )
        return l_filter

    change_list_filter_template = "admin/filter_listing.html"
    inlines = [ArtifactInline,]
    filter_horizontal = ('tags','metadata',)

    
    def get_queryset(self, request):
        query = Build.objects.all().prefetch_related('tags', 'metadata', 'metadata__category')
        if request.user.is_superuser:
            return query
        return query.filter(allowed_groups__in = request.user.groups.values('pk'))


    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super(BuildAdmin, self).get_form(request, obj, **kwargs)
        elif request.user.groups.filter(pk__in=obj.allowed_groups.values('pk')).exists():
            return super(BuildAdmin, self).get_form(request, obj, **kwargs)


    def get_readonly_fields(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return ()
        else:
            return ('metadata',)


    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('name', 'metadata', 'tags', 'allowed_groups',)
        else:
            return ('name','metadata','tags',)
       
