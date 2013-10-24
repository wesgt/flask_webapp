from flask import Blueprint, current_app


push_notification = Blueprint('push_notification', __name__,
                template_folder='templates')


@push_notification.route('/devices/<token>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def push_notification_receipts_verify(token):
    current_app.logger.debug('push_notification token {0}'.format(token))
    return 'push_notification token {0}'.format(token)


@push_notification.route('/message', methods=['POST'])
def push_notification_message():
    current_app.logger.debug('push_notification message')
    return 'push_notification token'
