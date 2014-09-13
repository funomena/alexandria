from datastore.models import AutoAccessRule, KeepRule 
from django.contrib import admin

@admin.register(AutoAccessRule)
class AutoAccessRuleAdmin(admin.ModelAdmin):
    fieldsets = (
                (
                    None,
                    {
                        "fields": ('required_metadata',),
                        "description": "If builds have any of these metadata..."
                    }
                ),
                (
                    None,
                    {
                        "fields": ('required_tags',),
                        "description": "...or any of these tags..."
                    }
                ),
                (
                    None,
                    {
                        "fields": ('all_access_override',),
                        "description": "...or this box is checked..."
                    }
                ),
                (
                    None,
                    {
                        "fields": ('groups',),
                        "description": "...automatically grant access to these groups."
                    }
                ),
            )


@admin.register(KeepRule)
class KepRuleAdmin(admin.ModelAdmin):
    pass
