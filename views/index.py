import os
from pyramid.response import Response

def index(request):
    here = os.path.dirname(__file__)
    index_html = os.path.join(here, '../app/template.html')
    openFile = open(index_html)
    data = openFile.read()
    return Response(data, content_type='text/html')

def partials(request):
	partial = request.matchdict['partial']
	print("subpath: " + request.subpath)

def includeme(config):
    config.add_route('index', '/')
    config.add_view(index, route_name='index')

    config.add_route('partials', '/partials/{partial}')
    config.add_view(partials, route_name='partials')

    config.add_static_view(name='js', path='../static/js')
    config.add_static_view(name='css', path='../static/css')