import unittest
from flask import json
import webapp
from webapp.push_notification import notify, ResultType
from webapp.database import db_session, drop_all_table


class PushNotificationTestCase(unittest.TestCase):

    def setUp(self):
        app = webapp.create_app('config_testing.cfg')
        app.config['TESTING'] = True
        app.register_blueprint(notify, url_prefix='/notify')
        self.client = app.test_client()

    def tearDown(self):
        if db_session:
            db_session.remove()

        drop_all_table()

    def setUpClass():
        pass

    def tearDownClass():
        pass

    # register devices token
    def test_register_devices_token_return_correct(self):
        user_id = '1'
        token = 'test_token'
        register_rv = self.client.put(
            '/notify/users/' + user_id + '/devices',
            data=dict(token=token, game_id='test_game'),
            follow_redirects=False)

        register_result = json.loads(str(register_rv.data, 'utf-8'))
        self.assertEqual(ResultType.REGISTER_DIVICES_TOKEN_SUCCESS,
                         register_result['result'])

    def test_register_devices_token_return_empty_token_error(self):
        user_id = '1'
        token = ''
        register_rv = self.client.put(
            '/notify/users/' + user_id + '/devices',
            data=dict(token=token, game_id='test_game'),
            follow_redirects=False)

        register_result = json.loads(str(register_rv.data, 'utf-8'))
        self.assertEqual(ResultType.REGISTER_DIVICES_EMPTY_TOKEN_ERROR,
                         register_result['result'])

    def test_simple_notification_return_correct(self):
        message = 'Oh no! Server\'s Down!'

        push_notification_rv = self.client.post(
            '/notify/message',
            data=dict(message=message),
            follow_redirects=False)

        push_notification_result = json.loads(str(push_notification_rv.data,
                                              'utf-8'))

        self.assertEqual(ResultType.PUSH_NOTIFICATION_SUCCESS,
                         push_notification_result['result'])
        pass
