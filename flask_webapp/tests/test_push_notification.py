import unittest
from flask import json
import webapp
from webapp.push_notification import push_notification, ResultType


class PushNotificationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()
        pass

    def tearDown(self):
        pass

    def setUpClass():
        webapp.app = webapp.create_app('config.cfg')
        webapp.app.config['TESTING'] = True
        webapp.app.register_blueprint(
            push_notification, url_prefix='/push_notification')
        pass

    def tearDownClass():
        pass

    #register devices token
    def test_register_devices_token_return_correct(self):
        user_id = '1'
        token = 'test_token'
        register_rv = self.app.put(
            '/push_notification/users/' + user_id + '/devices', data=dict(token=token),
            follow_redirects=False)

        register_result = json.loads(str(register_rv.data, 'utf-8'))
        self.assertEqual(ResultType.REGISTER_DIVICES_TOKEN_SUCCESS,
                         register_result['result'])

    def test_register_devices_token_return_empty_token_error(self):
        user_id = '1'
        token = ''
        register_rv = self.app.put(
            '/push_notification/users/' + user_id + '/devices', data=dict(token=token),
            follow_redirects=False)

        register_result = json.loads(str(register_rv.data, 'utf-8'))
        self.assertEqual(ResultType.REGISTER_DIVICES_EMPTY_TOKEN_ERROR,
                         register_result['result'])

    def test_push_notification_return_correct(self):
        pass
