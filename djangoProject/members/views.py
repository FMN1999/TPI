from django.http import HttpResponse
from django.template import loader

def members(request):
  template = loader.get_template('voley-connect.html')
  return HttpResponse(template.render())
