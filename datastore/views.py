from django.shortcuts import render
from rest_framework import renderers, viewsets
from datastore.serializers import MetadataCategorySerializer, MetadataValueSerializer
from datastore.serializers import TagSerializer, BuildSerializer
from datastore.serializers import ArtifactCategorySerializer, ArtifactSerializer
from datastore.models import MetadataCategory, MetadataValue, Tag
from datastore.models import ArtifactCategory, Artifact, Build
from rest_framework.response import Response


class MetadataCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetadataCategory.objects.all()
    serializer_class = MetadataCategorySerializer


class MetadataValueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetadataValue.objects.all()
    serializer_class = MetadataValueSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArtifactCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArtifactCategory.objects.all()
    serializer_class = ArtifactCategorySerializer


class BuildViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Build.objects.all()
    serializer_class = BuildSerializer

"""
    def create(self, request):
        d = request.DATA
        print d
        if len(d.get('metadata', [])) == 0:
            return Response({'error': "No metadata supplied"}, status=400)

        for cat in MetadataCategory.objects.filter(required=True):
            if not cat.slug in d['metadata'].keys():
                return Response({'error': "Missing required metadata: " + cat.slug}, status=400)

        metadata = []
        for c, v in d['metadata'].iteritems():
            if not MetadataCategory.objects.filter(slug=c).exists():
                return Response({'error': "Invalid metadata: " + c}, status=400)
            if not MetadataValue.objects.filter(category__slug=c, string_value=v).exists():
                cat = MetadataCategory.objects.get(slug=c)
                MetadataValue.objects.create(category=cat, string_value=v)
            metadata.append({'category': c, 'string_value': v})
        
        tag_list = d.get('tags', [])
        for t in tag_list:
            if not Tag.objects.filter(value=t).exists():
                Tag.objects.create(value=t)

        data = {'name': d['name'], 'tags':tag_list, 'metadata':metadata}
        serializer = BuildSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.object)
        else:
            return Response(serializer.errors, status=400)

"""
