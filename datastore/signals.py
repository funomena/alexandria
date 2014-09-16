from django.db.models.signals import pre_delete, post_delete, post_save, pre_save
from django.dispatch import receiver
from datastore.models import MetadataCategory, MetadataValue, Tag, KeepRule
from datastore.models import ArtifactCategory, Artifact, Build, AutoAccessRule
import boto
from django.conf import settings


@receiver(post_save, sender=Build)
def execute_keep_rules(sender, instance, created, raw, using, update_fields, **kwargs):
    if KeepRule.objects.filter(active=True).exists():
        rule = KeepRule.objects.filter(active=True).latest('pk')
        try:
            exec(rule.keep_code)
        except Exception as e:
            rule.last_execution = str(e)
        else:
            rule.last_execution = "OK"
        rule.save()


@receiver(pre_delete, sender=Build)
def cleanup_orphaned_metadata(sender, **kwargs):
    for meta in kwargs['instance'].metadata.all():
        if meta.builds.count() < 1:
            meta.delete()


@receiver(pre_delete, sender=Build)
def cleanup_orphaned_tags(sender, **kwargs):
    for tag in kwargs['instance'].tags.all():
        if tag.builds.count() < 1:
            tag.delete()


@receiver(post_delete, sender=Build)
def cleanup_orphaned_artifacts(sender, **kwargs):
    for art in kwargs['instance'].artifacts.all():
        art.delete()


@receiver(post_delete, sender=Artifact)
def cleanup_stored_files(sender, **kwargs):
    s3 = boto.connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_ACCESS_SECRET)
    bucket = s3.get_bucket(settings.S3_BUCKET)
    key = bucket.get_key(kwargs['instance'].s3_key)
    if key is None:
        print "Key doesn't exist"
        return
    key.delete()

