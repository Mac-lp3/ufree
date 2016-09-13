import os
from pyramid.response import Response

def index(request):
    here = os.path.dirname(__file__)
    index_html = os.path.join(here, '../app/template.html')
    openFile = open(index_html)
    data = openFile.read()
    return Response(data, content_type='text/html')

def includeme(config):
    config.add_route('index', '/')
    config.add_view(index, route_name='index')