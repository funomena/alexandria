from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from emubaby.settings import ORG_NAME
from datastore.models import Build


@login_required
def index(request):
	latest_build = Build.objects.latest('pk')
	return TemplateResponse(request, 'index.html', {'org_name': ORG_NAME, 'latest_build': latest_build})


@login_required
def profile_page(request):
	return TemplateResponse(request, 'profile_page.html', {'user': request.user})

