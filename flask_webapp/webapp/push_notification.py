"""

    push notification :
    This module implements (register / delete) device token,
    and sand message to device by this token.

"""
import time
from os import path
import socket
import ssl
import json
import struct
import binascii
from flask import request, jsonify, Blueprint, current_app


notify = Blueprint('notify', __name__, template_folder='templates')


class ResultType:
    REGISTER_DEVICES_TOKEN_SUCCESS = 'success'
    REGISTER_DEVICES_EMPTY_TOKEN_ERROR = 'empty_token_error'
    PUSH_NOTIFICATION_SUCCESS = 'success'


@notify.route('/users/<user_id>/devices', methods=['PUT', 'DELETE'])
def register_devices_token(user_id=None):
    """

        (register / delete) device token.
        The token that come from device register to APNs.

    """

    from webapp.models import DeviceToken

    if request.method == 'PUT':

        if not request.form['token']:
            return jsonify(result=ResultType.REGISTER_DEVICES_EMPTY_TOKEN_ERROR)

        device_token = DeviceToken(user_id, request.form['game_id'], request.form['token'])
        device_token.save()

        return jsonify(result=ResultType.REGISTER_DEVICES_TOKEN_SUCCESS)

    elif request.method == 'DELETE':
        pass


@notify.route('/message/<notification_type>', methods=['POST'])
def push_notification_message(notification_type=None):
    """

    Push message to APNs, and then APNs send message to device.
    The cert_file generate by 'openssl pkcs12 -in Certificates.p12 -out MyApplication.pem -nodes -clcerts'.

    """

    APNS_DEVELOPMENT_URL = 'gateway.sandbox.push.apple.com'
    APNS_PRODUCTION_URL = 'gateway.push.apple.com'
    APNS_PORT = 2195

    apns_url = APNS_DEVELOPMENT_URL if current_app.config['DEBUG'] else APNS_PRODUCTION_URL

    the_host = (apns_url, APNS_PORT)

    # prepare certification file
    push_file_path = path.abspath(path.dirname(__file__))
    the_certfile = path.join(push_file_path, 'config/' + current_app.config['CERT_FILE_NAME'])

    #device_token = 'C009AEB794E40D6320B019444EC7C8E0B271D9C1950BA887B442757C746B8EC5'

    device_tokens = ['03DC5621458E1F300483DE51BD89A8F4A266A7D966C403085372F7668CF24E21',
                     '03DC5621458E1F300483DE51BD89A8F4A266A7D966C403085372F7668CF24E21',
                     '03DC5621458E1F300483DE51BD89A8F4A266A7D966C403085372F7668CF24E21']
    #device_tokens = ['03DC5621458E1F300483DE51BD89A8F4A266A7D966C403085372F7668CF20000']
    notification_data = _create_notification_data(notification_type, request.form['message'],
                                                  device_tokens)

    ssl_sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                               certfile=the_certfile, ssl_version=ssl.PROTOCOL_SSLv23)

    ssl_sock.connect(the_host)

    for notification in notification_data:
        ssl_sock.send(notification)

    if notification_type == 'enhanced':
        try:
            ssl_sock.settimeout(1)
            recv_data = ssl_sock.recv(1024)
            command, status, identifier = struct.unpack_from('!BBI', recv_data, 0)
            print(recv_data)

        except socket.timeout as e:
            print(e.__class__)

    ssl_sock.close()
    return jsonify(result=ResultType.PUSH_NOTIFICATION_SUCCESS)


def _create_notification_data(notification_type, message, device_tokens):
    """

        notification format: refer Local and Push Notification Programming Guide
        payload need encode 'utf-8'

    """
    notification_data = []

    # prepare notification data
    the_pay_load = {
        'aps': {
            'alert': message,
            'sound': 'k1DiveAlarm.caf',
            'badge': 0,
        },
    }
    data = json.dumps(the_pay_load)
    payload = data.encode('utf-8')

    simple_format = '!BH32sH{0}s'.format(len(payload))
    enhanced_format = '!BIIH32sH{0}s'.format(len(payload))

    if notification_type == 'simple':
        for device_token in device_tokens:
            byte_token = binascii.unhexlify(device_token)
            notification_data.append(struct.pack(simple_format, 0, 32, byte_token, len(payload), payload))

    elif notification_type == 'enhanced':
        for device_token in device_tokens:
            identifier = int(time.time())
            expiry = int(time.time()) + 3600
            byte_token = binascii.unhexlify(device_token)
            notification_data.append(struct.pack(enhanced_format, 1, identifier, expiry, 32, byte_token,
                                                 len(payload), payload))

    return notification_data