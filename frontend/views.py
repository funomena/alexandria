from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from emubaby.settings import ORG_NAME
from datastore.models import *


@login_required
def index(request):
	num_builds = Build.objects.count()
	num_accessible_builds = Build.objects.count()
	return TemplateResponse(request, 'index.html', {'org_name': ORG_NAME, 'num_builds': num_builds, 'accessible_builds': num_accessible_builds})


@login_required
def latest(request):
	latest_build = Build.objects.latest('created')
	latest_starred = Build.objects.filter(starred=True).latest('created')
	return TemplateResponse(request, 'latest.html', {'latest_build': latest_build, 'latest_starred': latest_starred})


@login_required
def build_page(request, build_id):
	build = Build.objects.get(id=build_id)
	installers = Artifact.objects.get(a_type__is_installer=True, build__id=build_id)
	artifacts = Artifact.objects.get(a_type__is_installer=False, build__id=build_id)
	metadata_set = MetaData.objects.get(category__is_extra_data=False, build_id=build_id)
	extra_data_set = MetaData.objects.get(category__is_extra_data=True, build_id=build_id)
	return TemplateResponse(request, 'build.html', {'build': build, 'installers': installers, 'artifacts': artifacts, 'metadata_set': metadata_set, 'extra_data_set': extra_data_set})


@login_required
def profile_page(request):
	return TemplateResponse(request, 'profile_page.html', {'user': request.user})

