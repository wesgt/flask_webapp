from flask import request, jsonify, Blueprint, current_app


push_notification = Blueprint('push_notification', __name__,
                template_folder='templates')

class ResultType:
    REGISTER_DIVICES_TOKEN_SUCCESS = 'success'
    REGISTER_DIVICES_EMPTY_TOKEN_ERROR = 'empty_token_error'

@push_notification.route('/users/<user_id>/devices', methods=['PUT', 'DELETE'])
def register_devices_token(user_id=None):
    """

        (register / delete) device token,
        and then sand message to device by this token.

    """

    if request.method == 'PUT':

        if not request.form['token']:
            return jsonify(result=ResultType.REGISTER_DIVICES_EMPTY_TOKEN_ERROR)

        return jsonify(result=ResultType.REGISTER_DIVICES_TOKEN_SUCCESS)

    elif request.method == 'DELETE':
        pass



@push_notification.route('/message', methods=['POST'])
def push_notification_message():
    current_app.logger.debug('push_notification message')
    return 'push_notification token'
