import urllib
from flask import request, Blueprint, current_app, json, jsonify


iap = Blueprint('iap', __name__, template_folder='templates')


class ResultType:
    VERIFY_SECCESS = 'verify_success'
    VERIFY_FAIL = 'verify_fail'


@iap.route('/receipts/verify', methods=['POST', 'GET'])
def iap_receipts_verify():
    """

        Validating Receipts With the App Store

    """

    SAND_BOX_VERIFY_URL = "https://sandbox.itunes.apple.com/verifyReceipt"
    PRODUCTION_VERIFY_URL = "https://buy.itunes.apple.com/verifyReceipt"

    verify_url = SAND_BOX_VERIFY_URL if current_app.config['DEBUG'] else PRODUCTION_VERIFY_URL

    result = {}
    result['receipt-data'] = request.form['receipt_data']
    request_data = str.encode(json.dumps(result))

    iap_request = urllib.request.Request(url=verify_url,
                                         data=request_data, method='POST')
    iap_response = urllib.request.urlopen(iap_request)

    verify_result = json.loads(str(iap_response.read(), 'utf-8'))
    #current_app.logger.debug('verify_result : {0}'.format(verify_result))

    if iap_response.status != 200:
        return jsonify(result=ResultType.VERIFY_FAIL)

    if verify_result['status'] == 0:
        return jsonify(result=ResultType.VERIFY_SECCESS)
    else:
        return jsonify(result=ResultType.VERIFY_FAIL)

