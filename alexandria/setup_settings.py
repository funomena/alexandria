"""
Django settings for alexandria project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from alexandria.settings import *

INSTALLED_APPS = (
    'django.contrib.auth',
    'datastore',
    'django.contrib.contenttypes',
) 
