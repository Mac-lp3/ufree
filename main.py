from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

if __name__ == '__main__':
    config = Configurator()
    config.include('views.index')
    config.include('views.api')
    config.add_static_view(name='css', path='static/css')
    config.add_static_view(name='js', path='static/js')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()