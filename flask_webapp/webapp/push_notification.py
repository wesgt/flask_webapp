"""

    push notification :
    This module implements (register / delete) device token,
    and sand message to device by this token.

"""

from flask import request, jsonify, Blueprint, current_app


notify = Blueprint('notify', __name__, template_folder='templates')


class ResultType:
    REGISTER_DIVICES_TOKEN_SUCCESS = 'success'
    REGISTER_DIVICES_EMPTY_TOKEN_ERROR = 'empty_token_error'
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
            return jsonify(result=ResultType.REGISTER_DIVICES_EMPTY_TOKEN_ERROR)

        device_token = DeviceToken(user_id, request.form['game_id'], request.form['token'])
        device_token.save()

        return jsonify(result=ResultType.REGISTER_DIVICES_TOKEN_SUCCESS)

    elif request.method == 'DELETE':
        pass


@notify.route('/message', methods=['POST'])
def push_notification_message():

    return jsonify(result=ResultType.PUSH_NOTIFICATION_SUCCESS)
