import urllib
import base64
from flask import request, Blueprint, current_app, json, jsonify


iap = Blueprint('iap', __name__, template_folder='templates')


class ResultType:
    VERIFY_SUCCESS = 'verify_success'
    VERIFY_FAIL = 'verify_fail'


@iap.route('/receipts/verify', methods=['POST', 'GET'])
def iap_receipts_verify():
    """ Validating Receipts With the App Store """

    from webapp.models import IAPVerifyData

    SAND_BOX_VERIFY_URL = "https://sandbox.itunes.apple.com/verifyReceipt"
    PRODUCTION_VERIFY_URL = "https://buy.itunes.apple.com/verifyReceipt"

    verify_url = SAND_BOX_VERIFY_URL if current_app.config['DEBUG'] else PRODUCTION_VERIFY_URL

    result = None
    try:
        result = {'receipt-data': str(base64.b64encode(request.data), 'utf-8')}
    except Exception as e:
        print(e.__class__)

    request_data = str.encode(json.dumps(result))

    iap_request = urllib.request.Request(url=verify_url,
                                         data=request_data, method='POST')
    iap_response = urllib.request.urlopen(iap_request)

    verify_result = json.loads(str(iap_response.read(), 'utf-8'))
    #current_app.logger.debug('verify_result : {0}'.format(verify_result))

    if iap_response.status != 200:
        return jsonify(result=ResultType.VERIFY_FAIL)

    if verify_result['status'] == 0:

        # check ios6 or ios7

        if _is_ios6(verify_result['receipt']):

            iap_verify_data = IAPVerifyData.query.filter(IAPVerifyData.transaction_id ==
                                                         verify_result['receipt']['original_transaction_id']).first()

            if iap_verify_data:
                iap_verify_data.transaction_id = verify_result['receipt']['transaction_id']
                iap_verify_data.purchase_date = verify_result['receipt']['purchase_date']
                iap_verify_data.save()

            else:
                iap_verify_data = IAPVerifyData.create_for_ios6('ooo', verify_result['receipt'])
                iap_verify_data.save()
        else:
            in_app_result = verify_result['receipt']['in_app'][0]
            print('test id : {0} '.format(in_app_result['original_transaction_id']))
            iap_verify_data = IAPVerifyData.query.filter(
                IAPVerifyData.transaction_id == in_app_result['original_transaction_id']).first()

            if iap_verify_data:
                iap_verify_data.transaction_id = in_app_result['transaction_id']
                iap_verify_data.purchase_date = in_app_result['purchase_date']
                iap_verify_data.save()

            else:
                iap_verify_data = IAPVerifyData.create_for_ios7('ooo',
                                                                verify_result['receipt']['bundle_id'],
                                                                verify_result['receipt']['application_version'],
                                                                in_app_result)
                iap_verify_data.save()


        return jsonify(result=ResultType.VERIFY_SUCCESS)
    else:
        return jsonify(result=ResultType.VERIFY_FAIL)


def _is_ios6(receipt_data):

    if 'original_transaction_id' in receipt_data:
        return True

    else:
        return False