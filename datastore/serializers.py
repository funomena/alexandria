from datastore.models import MetadataCategory, MetadataValue, Tag
from datastore.models import ArtifactCategory, Artifact, Build
from rest_framework import serializers


class MetadataCategorySerializer(serializers.ModelSerializer):
    values = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = MetadataCategory
        read_only_fields = ('slug', 'friendly_name', 'required')
        lookup_field = 'slug'


# TODO: Make value field dynamic based on category type
# TODO: Remove string_value
class MetadataValueSerializer(serializers.ModelSerializer):
    category = MetadataCategorySerializer()
    builds = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
    string_value = serializers.CharField()

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
   
    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None: #update things
            return instance
        else:
            return Build(**attrs)
        
    class Meta:
        model = Build
        


