from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
	return TemplateResponse(request, 'default_body.html')


@login_required
def profile_page(request):
	return TemplateResponse(request, 'profile_page.html', {'user': request.user})