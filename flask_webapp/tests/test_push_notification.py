import unittest
from flask import json
import webapp
from webapp.push_notification import notify, ResultType


class PushNotificationTestCase(unittest.TestCase):

    def setUp(self):
        app = webapp.create_app('config_testing.cfg')
        app.config['TESTING'] = True
        app.register_blueprint(notify, url_prefix='/mobile/notify')
        self.client = app.test_client()

    def tearDown(self):
        from webapp.database import db_session, drop_all_table
        if db_session:
            db_session.remove()

        drop_all_table()

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # register devices token
    def test_register_devices_token_return_correct(self):
        user_id = '1'
        token = 'test_token'
        game_id = 'test_game'
        register_rv = self.client.put(
            '/mobile/notify/users/' + user_id + '/devices',
            data=dict(token=token, game_id=game_id),
            follow_redirects=False)

        register_result = json.loads(str(register_rv.data, 'utf-8'))
        self.assertEqual(ResultType.REGISTER_DEVICES_TOKEN_SUCCESS,
                         register_result['result'])

    def test_register_devices_token_return_empty_token_error(self):
        user_id = '1'
        token = ''
        game_id = 'test_game'
        register_rv = self.client.put(
            '/mobile/notify/users/' + user_id + '/devices',
            data=dict(token=token, game_id=game_id),
            follow_redirects=False)

        register_result = json.loads(str(register_rv.data, 'utf-8'))
        self.assertEqual(ResultType.REGISTER_DEVICES_EMPTY_TOKEN_ERROR,
                         register_result['result'])

    def test_simple_notification_return_correct(self):
        from webapp.models import DeviceToken

        # prepare test token on db
        device_token = DeviceToken('1', 'game_test', '03DC5621458E1F300483DE51BD89A8F4A266A7D966C403085372F7668CF24E21')
        device_token.save()
        device_token = DeviceToken('2', 'game_test', 'BF19A9937D1D1912C0801052F9FC2B78D70C8D21D9201B1E69AA2AA4F0EB770B')
        device_token.save()

        # push notification
        message = 'Oh no! Simple\'s Down!'

        push_notification_rv = self.client.post(
            '/mobile/notify/message/simple',
            data=dict(message=message),
            follow_redirects=False)

        push_notification_result = json.loads(str(push_notification_rv.data,
                                              'utf-8'))

        self.assertEqual(ResultType.PUSH_NOTIFICATION_SUCCESS,
                         push_notification_result['result'])

    def test_enhanced_notification_return_correct(self):
        from webapp.models import DeviceToken

        # prepare test token on db
        device_token = DeviceToken('1', 'game_test', '03DC5621458E1F300483DE51BD89A8F4A266A7D966C403085372F7668CF24E21')
        device_token.save()
        device_token = DeviceToken('2', 'game_test', 'BF19A9937D1D1912C0801052F9FC2B78D70C8D21D9201B1E69AA2AA4F0EB770B')
        device_token.save()

        # push notification
        message = 'Oh no! Enhanced\'s Down!'

        push_notification_rv = self.client.post(
            '/mobile/notify/message/enhanced',
            data=dict(message=message),
            follow_redirects=False)

        push_notification_result = json.loads(str(push_notification_rv.data,
                                              'utf-8'))

        self.assertEqual(ResultType.PUSH_NOTIFICATION_SUCCESS,
                         push_notification_result['result'])