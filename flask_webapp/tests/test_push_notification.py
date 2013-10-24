import unittest
from flask import json
import webapp
from webapp.push_notification import push_notification


class PushNotificationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()
        pass

    def tearDown(self):
        pass

    def setUpClass():
        webapp.app = webapp.create_app('config.cfg')
        webapp.app.config['TESTING'] = True
        webapp.app.register_blueprint(push_notification, url_prefix='/push_notification')
        pass

    def tearDownClass():
        pass

    def test_push_notification_return_correct(self):
        pass
