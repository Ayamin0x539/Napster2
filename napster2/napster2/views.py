from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request): # request parameter has host params (ip, etc)
    return render_to_response('index.html', {}, RequestContext(request))


