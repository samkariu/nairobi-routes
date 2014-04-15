"""
Using redirect route instead of simple routes since it supports strict_slash
Simple route: http://webapp-improved.appspot.com/guide/routing.html#simple-routes
RedirectRoute: http://webapp-improved.appspot.com/api/webapp2_extras/routes.html#webapp2_extras.routes.RedirectRoute
"""

import webapp2
from webapp2_extras.routes import RedirectRoute
from web import handlers
secure_scheme = 'https'

_routes = [
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    webapp2.Route('/routes/<route_type>', handlers.RouteListHandler, name='route-list'),
    webapp2.Route('/route/<route_type>/<route_name>', handlers.RouteHandler, name='route'),
    webapp2.Route('/stops/<route_type>/<route_name>', handlers.StopsHandler, name='stops')
]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)