from django.template.response import SimpleTemplateResponse, TemplateResponse
# Create your views here.


def index(request):
	return SimpleTemplateResponse('default_body.html')


def profile_page(request):
	return TemplateResponse(request, 'profile_page.html', {'user': request.user})