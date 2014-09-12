from datastore.models import MetadataCategory, MetadataValue, Tag
from datastore.models import ArtifactCategory, Artifact, Build
from rest_framework import serializers


class MetadataCategorySerializer(serializers.ModelSerializer):
    values = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = MetadataCategory
        read_only_fields = ('slug', 'friendly_name', 'required')
        lookup_field = 'slug'


class MetadataValueSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="slug")
    builds = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
    string_value = serializers.CharField(write_only=True)
    value = serializers.Field(source='value')

    class Meta:
        model = MetadataValue
        lookup_field = 'pk'


class TagSerializer(serializers.ModelSerializer):
    builds = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Tag
        read_only_fields = ('value',)


class ArtifactCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactCategory
        read_only_fields = ('slug', 'friendly_name', 'extension')


class ArtifactSerializer(serializers.ModelSerializer):
    category = ArtifactCategorySerializer()
    build = serializers.RelatedField()
    class Meta:
        model = Artifact


class BuildSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=64)
    tags = serializers.SlugRelatedField(many=True, slug_field='value')
    metadata = MetadataValueSerializer(many=True)
    artifacts = serializers.PrimaryKeyRelatedField(many=True)       

    def validate_metadata(self, attrs, source):
        metadata = attrs[source]
        slugs = []
        for m in metadata:
            if m.category.slug in slugs:
                raise serializers.ValidationError("Duplicate metadata: " + c.slug)
            slugs.append(m.category.slug)
        for c in MetadataCategory.objects.filter(required=True):
            if not c.slug in slugs:
                raise serializers.ValidationError("Missing required metadata: " + c.slug)
        return attrs
     
    class Meta:
        model = Build
        exclude = ('allowed_groups', )
