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
class KeepRuleAdmin(admin.ModelAdmin):
    fieldsets = (
            (
                None,
                {
                    "fields": ("keep_code",),
                    "description": "Python code that gets executed after each\
                                    build is saved.  You'll need to do your own\
                                    imports from datastore.models to get access\
                                    to models.  Also, don't do stupids."
                }
            ),
            (
                None,
                {
                    "fields": ("active", ),
                    "description": "Whether this code should be executed.\
                                    Allows you to keep rules around when you\
                                    don't want to use them."
                }
            ),
            (
                None,
                {
                    "fields": ("last_execution",),
                    "description": "The execution status of the last time this\
                                    code was run.  Either the contents of the\
                                    error that was thrown or 'OK' if everything\
                                    was fine"
                }
            ),
        )

    readonly_fields = ('last_execution', )
