from flask import Blueprint, current_app


iap = Blueprint('iap', __name__,
                template_folder='templates')


@iap.route('/receipts/verify', methods=['POST', 'GET'])
def iap_receipts_verify():
    current_app.logger.debug('iap_receipts_verify')
    return 'iap_receipts_verify '
