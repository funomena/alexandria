from django.template.response import SimpleTemplateResponse
# Create your views here.


def index(request):
	return SimpleTemplateResponse('default_body.html')