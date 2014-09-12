from django.shortcuts import render, redirect
from django.template.response import SimpleTemplateResponse
from rest_framework import renderers, viewsets
from datastore.serializers import MetadataCategorySerializer, MetadataValueSerializer
from datastore.serializers import TagSerializer, BuildSerializer
from datastore.serializers import ArtifactCategorySerializer, ArtifactSerializer
from datastore.models import MetadataCategory, MetadataValue, Tag
from datastore.models import ArtifactCategory, Artifact, Build
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class MetadataCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = MetadataCategory.objects.all()
    serializer_class = MetadataCategorySerializer


class MetadataValueViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = MetadataValue.objects.all()
    serializer_class = MetadataValueSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArtifactCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = ArtifactCategory.objects.all()
    serializer_class = ArtifactCategorySerializer


class BuildViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Build.objects.all()
    serializer_class = BuildSerializer


def handle_index(request):
    print request.user
    if request.user is None:
        return SimpleTemplateResponse("index.html")
    else:
        return redirect('/navigate/')

