import os
from pyramid.response import Response, FileResponse

here = os.path.dirname(__file__)

def index(request):
    index_html = os.path.join(here, '../client/src/index.html')
    openFile = open(index_html)
    data = openFile.read()
    return Response(data, content_type='text/html')

def bundle(request):
    bundle_js = os.path.join(here, '../client/dist/main.bundle.js')
    openFile = open(bundle_js)
    data = openFile.read()
    return Response(data, content_type='text/html')

def styles(request):
    styles_css = os.path.join(here, '../client/src/main.css')
    openFile = open(styles_css)
    data = openFile.read()
    return Response(data, content_type='text/html')

def landing_image(request):
    asset = os.path.join(here, '../client/src/assets/color-tablet.jpeg')
    return FileResponse(
        asset,
        request=request,
        content_type='image/jpeg'
    )

def includeme(config):
    config.add_route('index', '/')
    config.add_view(index, route_name='index')

    config.add_route('bundle', '/main.bundle.js')
    config.add_view(bundle, route_name='bundle')

    config.add_route('styles', '/main.css')
    config.add_view(styles, route_name='styles')

    config.add_route('landing_image', '/assets/color-tablet.jpeg')
    config.add_view(landing_image, route_name='landing_image')
