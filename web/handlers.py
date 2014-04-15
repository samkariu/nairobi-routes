# -*- coding: utf-8 -*-

"""
    A real simple app for using webapp2 with auth and session.

    It just covers the basics. Creating a user, login, logout
    and a decorator for protecting certain handlers.

    Routes are setup in routes.py and added in main.py
"""
import os
import csv
import httpagentparser
import json
import datetime
from boilerplate import models
from boilerplate.lib.basehandler import BaseHandler
from boilerplate.lib.basehandler import user_required


def getRouteList(route_type):
    ls = []
    curr_path = os.path.split(os.path.abspath(__file__))[0]
    route_path = os.path.join(os.path.split(curr_path)[0], 'static/routes/'+route_type)
    ls.extend(os.listdir(route_path))
    return ls

def read_csv_file(filename):
    ls = []
    input_file = csv.DictReader(open(filename))
    for row in input_file:
        ls.append(row)
    return ls

    

def RespondJSON(handler, data):
        """Generate a JSON response and return it to the client.
    
        Args:
          data: The data that will be converted to JSON to return.
        """
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        handler.response.headers['Content-Type'] = 'application/json'
        handler.response.out.write(json.dumps(data))
        

class SecureRequestHandler(BaseHandler):
    """
    Only accessible to users that are logged in
    """

    @user_required
    def get(self, **kwargs):
        user_session = self.user
        user_session_object = self.auth.store.get_session(self.request)

        user_info = models.User.get_by_id(long( self.user_id ))
        user_info_object = self.auth.store.user_model.get_by_auth_token(
            user_session['user_id'], user_session['token'])

        try:
            params = {
                "user_session" : user_session,
                "user_session_object" : user_session_object,
                "user_info" : user_info,
                "user_info_object" : user_info_object,
                "userinfo_logout-url" : self.auth_config['logout_url'],
                }
            return self.render_template('secure_zone.html', **params)
        except (AttributeError, KeyError), e:
            return "Secure zone error:" + " %s." % e
        
class RouteListHandler(BaseHandler):
    def get(self, route_type):
        route_list = getRouteList(route_type)
        output = {}
        output["routes"] = route_list
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(output))
        
class RouteHandler(BaseHandler):
    def get(self, route_type, route_name):
        curr_path = os.path.split(os.path.abspath(__file__))[0]
        file_path = 'static/routes/' + route_type + '/' + route_name + '/track.csv'
        route_path = os.path.join(os.path.split(curr_path)[0], file_path)
        output = read_csv_file(route_path)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(output))
        
class StopsHandler(BaseHandler):
    def get(self, route_type, route_name):
        curr_path = os.path.split(os.path.abspath(__file__))[0]
        file_path = 'static/routes/' + route_type + '/' + route_name + '/stops.csv'
        route_path = os.path.join(os.path.split(curr_path)[0], file_path)
        output = read_csv_file(route_path)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(output))