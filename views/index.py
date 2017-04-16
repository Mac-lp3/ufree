import os
from pyramid.response import Response

here = os.path.dirname(__file__)

def index(request):
    index_html = os.path.join(here, '../client/src/index.html')
    openFile = open(index_html)
    data = openFile.read()
    return Response(data, content_type='text/html')

def bundle(request):
    bundle_html = os.path.join(here, '../client/dist/main.bundle.js')
    openFile = open(bundle_html)
    data = openFile.read()
    return Response(data, content_type='text/html')

def includeme(config):
    config.add_route('index', '/')
    config.add_view(index, route_name='index')

    config.add_route('bundle', '/main.bundle.js')
    config.add_view(bundle, route_name='bundle')
