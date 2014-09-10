from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from datastore.models import MetadataCategory, MetadataValue, Tag
from datastore.models import ArtifactCategory, Artifact, Build
import boto
from django.conf import settings


@receiver(pre_delete, sender=Build)
def cleanup_orphaned_metadata(sender, instance, using):
    for meta in instance.metadata:
        if len(meta.builds) <= 1:
            meta.delete()


@receiver(pre_delete, sender=Build)
def cleanup_orphaned_tags(sender, instance, using):
    for tag in instance.tags:
        if len(tag.builds) <= 1:
            tag.delete()


@receiver(post_delete, sender=Build)
def cleanup_orphaned_artifacts(sender, instance, using):
    for art in build.artifacts:
        art.delete()


@receiver(post_delete, sender=Artifact)
def cleanup_stored_files(sender, instance, using):
    s3 = boto.connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_ACCESS_SECRET)
    bucket = s3.get_bucket(settings.S3_BUCKET)
    key = bucket.get_key(instance.key_name)
    key.delete()

