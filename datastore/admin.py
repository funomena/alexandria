from django.contrib import admin 
from datastore.models import *

admin.site.register(Build)
admin.site.register(MetaDataCategory)
admin.site.register(MetaData)
admin.site.register(ArtifactType)
admin.site.register(Artifact)
