from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from datastore.models import MetadataCategory, MetadataValue, Tag
from datastore.models import ArtifactCategory, Artifact, Build, AutoAccessRule
from datastore.serializers import BuildSerializer, ArtifactSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BuildNotification(APIView):

    def post(self, request, format=None):
        authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
        permission_classes = (IsAuthenticated,)
        name = request.DATA.get("name", "")
        metadata = request.DATA.get("metadata", {})
        tags = request.DATA.get("tags", [])
 
        for req_cat in MetadataCategory.objects.filter(required=True):
            if not req_cat.slug in metadata.keys():
                return Response({'error': "Missing required metadata: " + req_cat.slug}, status=400)

        for c, v in metadata.iteritems():
            if not MetadataCategory.objects.filter(slug=c).exists():
                return Response({'error': "Invalid metadata: " + c}, status=400)

        b = Build.objects.create(name=name)

        for t in tags:
            tag, created = Tag.objects.get_or_create(value=t)
            b.tags.add(tag) 

        for c, v in metadata.iteritems():
            cat = MetadataCategory.objects.get(slug=c)
            meta, created = MetadataValue.objects.get_or_create(category=cat, string_value=v)
            b.metadata.add(meta)

        m = AutoAccessRule.objects.filter(required_metadata__pk__in=b.metadata.values('pk'))
        t = AutoAccessRule.objects.filter(required_tags__pk__in=b.tags.values('pk'))
        all_access = AutoAccessRule.objects.filter(all_access_override=True)
        all_rules = (m | t) | all_access
        for rule in all_rules:
            b.allowed_groups.add(rule.groups)

        b.save()
        serializer = BuildSerializer(b)
        
        return Response(serializer.data)


