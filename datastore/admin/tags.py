from datastore.models import Tag
from django.contrib import admin

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
