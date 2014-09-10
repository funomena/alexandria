from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from datastore.models import MetadataCategory, MetadataValue, Tag
from datastore.models import ArtifactCategory, Artifact, Build
from datastore.serializers import BuildSerializer, ArtifactSerializer
import boto, uuid
from django.conf import settings
from django.shortcuts import redirect


class BuildNotification(APIView):

    def post(self, request, format=None):
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

        b.save()
        serializer = BuildSerializer(b)
        
        return Response(serializer.data)


class ArtifactUpload(APIView):

    def put(self, request, format=None):
        data = request.DATA
        cat = data.get("category", "")
        if cat == "":
            return Response({'error': "Missing artifact category"}, status=400)
        if not ArtifactCategory.objects.filter(slug=cat).exists():
            return Response({'error': "Invalid artifact category: " + cat}, status=400)        

        size = data.get("size", 0)
        if size == 0:
            return Response({'error': "No file size supplied"}, status=400)
        
        md5_hash = data.get("checksum", "")
        if md5_hash == "":
            return Response({'error': "No checksum supplied"}, status=400)
    
        b_id = data.get("build", -1)
        if b_id == -1:
            return Response({'error': "No build id supplied"}, status=400)
        if not Build.objects.filter(pk=b_id).exists():
            return Response({'error': "Invalid build id: " + b_id}, status=400)        

        key_name = str(uuid.uuid4())
        category = ArtifactCategory.objects.get(slug=cat)
        build = Build.objects.get(pk=b_id)
        if Artifact.objects.filter(category=category, build=build).exists():
            return Response({'error': cat + " already exists for build " + b_id}, status=400)

        artifact = Artifact.objects.create( category=category, build=build, 
                                            s3_key=key_name, file_size=size,
                                            md5_hash=md5_hash)
        
        s3 = boto.connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_ACCESS_SECRET)
        bucket = settings.S3_BUCKET
        url = s3.generate_url(300, 'PUT', bucket, key_name)
        return Response({'url': url}) 
   
 
    """ Once the user has PUT the file up to S3, recieves a confirmation signal """
    def patch(self, request, format=None):
        data = request.DATA
        cat = data.get("category", "")
        if cat == "":
            return Response({'error': "Missing artifact category"}, status=400)
        if not ArtifactCategory.objects.filter(slug=cat).exists():
            return Response({'error': "Invalid artifact category: " + cat}, status=400)        

        b_id = data.get("build", -1)
        if b_id == -1:
            return Response({'error': "No build id supplied"}, status=400)
        if not Build.objects.filter(pk=b_id).exists():
            return Response({'error': "Invalid build id: " + b_id}, status=400)        

        category = ArtifactCategory.objects.get(slug=cat)
        build = Build.objects.get(pk=b_id)
        if not Artifact.objects.filter(category=category, build=build).exists():
            return Response({'error': cat + " does not exist for build " + b_id}, status=400)
        
        artifact = Artifact.objects.get(category=category, build=build)

        s3 = boto.connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_ACCESS_SECRET)
        bucket = settings.S3_BUCKET
        key_name = artifact.s3_key
        key = s3.get_bucket(bucket).get_key(key_name)
        md5 = key.etag.strip('"')
        if md5 != artifact.md5_hash:
            artifact.delete()
            return Response({'error': "Checksums do not match! Supplied: " 
                                    + artifact.md5_hash + " Stored: " + md5},
                                    status=400)
       
        artifact.verified = True 
        serializer = ArtifactSerializer(artifact)
        return Response(serializer.data, status=201)
