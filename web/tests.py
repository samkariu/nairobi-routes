'''
Run the tests using testrunner.py script in the project root directory.

Usage: testrunner.py SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules

Options:
  -h, --help  show this help message and exit

'''
import unittest
import webapp2
import os
import logging
from google.appengine.ext import testbed

from mock import Mock
from mock import patch

import boilerplate
from boilerplate import models
from boilerplate import config as boilerplate_config
import config
import handlers
from boilerplate import routes
from boilerplate import routes as boilerplate_routes
from boilerplate.lib import utils
from boilerplate.lib import captcha
from boilerplate.lib import i18n
from boilerplate.lib import test_helpers

# setting HTTP_HOST in extra_environ parameter for TestApp is not enough for taskqueue stub
os.environ['HTTP_HOST'] = 'localhost'

# globals
network = False

# mock Internet calls
if not network:
    i18n.get_territory_from_ip = Mock(return_value=None)


class AppTest(unittest.TestCase, test_helpers.HandlerHelpers):
    def setUp(self):

        # create a WSGI application.
        webapp2_config = boilerplate_config.config
        webapp2_config.update(config.config)
        self.app = webapp2.WSGIApplication(config=webapp2_config)
        routes.add_routes(self.app)
        boilerplate_routes.add_routes(self.app)
        #self.testapp = webtest.TestApp(self.app, extra_environ={'REMOTE_ADDR' : '127.0.0.1'})
        
        # use absolute path for templates
        self.app.config['webapp2_extras.jinja2']['template_path'] =  [os.path.join(os.path.dirname(boilerplate.__file__), '../templates'), os.path.join(os.path.dirname(boilerplate.__file__), 'templates')]

        # activate GAE stubs
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
        self.taskqueue_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
        self.testbed.init_user_stub()

        self.headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) Version/6.0 Safari/536.25',
                        'Accept-Language' : 'en_US'}

        # fix configuration if this is still a raw boilerplate code - required by test with mails
        if not utils.is_email_valid(self.app.config.get('contact_sender')):
            self.app.config['contact_sender'] = "noreply-testapp@example.com"
        if not utils.is_email_valid(self.app.config.get('contact_recipient')):
            self.app.config['contact_recipient'] = "support-testapp@example.com"

    def tearDown(self):
        self.testbed.deactivate()

    def test_config_environment(self):
        self.assertEquals(self.app.config.get('environment'), 'testing')
        
    def test_route_path(self):
        path = os.path.split(os.path.abspath(__file__))[0]
        route_path = os.path.join(os.path.split(path)[0], 'static/routes')
        print route_path
        self.assert_(os.path.isdir(route_path), "No route directory")
        
    def test_route_list(self):
        ls = []
        curr_path = os.path.split(os.path.abspath(__file__))[0]
        route_path = os.path.join(os.path.split(curr_path)[0], 'static/routes')
        ls.extend(os.listdir(route_path))
        self.assertGreater(len(ls), 0, "No routes")
        
    def test_csv_reader(self):
        curr_path = os.path.split(os.path.abspath(__file__))[0]
        route_path = os.path.join(os.path.split(curr_path)[0], 'static/routes/Rounda_Kayole_17A/track.csv')
        output = handlers.read_csv_file(route_path)
        self.assertGreater(len(output), 0, "Read failed")

class ModelTest(unittest.TestCase):
    def setUp(self):

        # activate GAE stubs
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()


if __name__ == "__main__":
    unittest.main()
