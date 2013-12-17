import urllib
import base64
from flask import request, Blueprint, current_app, json, jsonify
from webapp.token import create_token, generate_hash_code, decode_token


iap = Blueprint('iap', __name__, template_folder='templates')

SAND_BOX_VERIFY_URL = "https://sandbox.itunes.apple.com/verifyReceipt"
PRODUCTION_VERIFY_URL = "https://buy.itunes.apple.com/verifyReceipt"
APP_SECRET_KEY = '123456789'


class ResultType:
    VERIFY_SUCCESS = 'succ'
    VERIFY_FAIL = 'fail'
    TOKEN_INVALID_ERROR = 'inva'
    TOKEN_EXPIRE_ERROR = 'expi'
    TOKEN_NO_EXIST_ERROR = 'noex'


@iap.route('/receipts/verify', methods=['POST', 'GET'])
def iap_receipts_verify():
    """ Validating Receipts With the App Store

    send receipt to apple, and then return token to client

    """

    verify_url = SAND_BOX_VERIFY_URL if current_app.config['DEBUG'] else PRODUCTION_VERIFY_URL

    #result = {'receipt-data': str(base64.b64encode(request.data), 'utf-8')}
    #print('reslt : {0}'.format(result))
    result = {'receipt-data': request.form['receipt_data']}
    request_data = str.encode(json.dumps(result))
    udid = request.form['udid']

    # post request to verify
    iap_request = urllib.request.Request(url=verify_url, data=request_data, method='POST')
    iap_response = urllib.request.urlopen(iap_request)

    verify_result = json.loads(str(iap_response.read(), 'utf-8'))
    #current_app.logger.debug('verify_result : {0}'.format(verify_result))

    if iap_response.status != 200:
        return jsonify(result=ResultType.VERIFY_FAIL)

    if verify_result['status'] == 0:
        iap_verify_data = _backup_verify_data(verify_result, udid)

        return create_token(ResultType.VERIFY_SUCCESS, APP_SECRET_KEY,
                            udid, iap_verify_data.verify_date,
                            iap_verify_data.transaction_id)

    else:
        return str.encode(ResultType.VERIFY_FAIL)


def _is_ios6(receipt_data):
    if 'original_transaction_id' in receipt_data:
        return True

    else:
        return False


def _backup_verify_data(verify_result, udid):
    """backup verify data to database

    Find verify data from database by 'original_transaction_id'.
    If have verify data, and then update.
    If not have verify data. and then add new.

    """
    from webapp.models import IAPVerifyData

    # check ios6 or ios7
    if _is_ios6(verify_result['receipt']):

        iap_verify_data = IAPVerifyData.query.filter(IAPVerifyData.transaction_id ==
                                                     verify_result['receipt']['original_transaction_id']).first()

        if iap_verify_data:
            iap_verify_data.transaction_id = verify_result['receipt']['transaction_id']
            iap_verify_data.purchase_date = verify_result['receipt']['purchase_date']
            iap_verify_data.save()

        else:
            iap_verify_data = IAPVerifyData.create_for_ios6(udid, verify_result['receipt'])
            iap_verify_data.save()
    else:
        in_app_result = verify_result['receipt']['in_app'][0]
        iap_verify_data = IAPVerifyData.query.filter(
            IAPVerifyData.transaction_id == in_app_result['original_transaction_id']).first()

        if iap_verify_data:
            iap_verify_data.transaction_id = in_app_result['transaction_id']
            iap_verify_data.purchase_date = in_app_result['purchase_date']
            iap_verify_data.save()

        else:
            iap_verify_data = IAPVerifyData.create_for_ios7(udid,
                                                            verify_result['receipt']['bundle_id'],
                                                            in_app_result)
            iap_verify_data.save()

    return iap_verify_data


@iap.route('/token/verify', methods=['POST', 'GET'])
def iap_token_verify():
    """ iap token verify """

    from datetime import datetime
    from webapp.models import IAPVerifyData

    client_token = decode_token(request.data)

    iap_verify_data = IAPVerifyData.query.filter(
        IAPVerifyData.transaction_id == client_token.transaction_id,
        IAPVerifyData.udid == client_token.udid
    ).first()

    if iap_verify_data is None:
        return str.encode(ResultType.TOKEN_NO_EXIST_ERROR)

    # check time valid
    if client_token.verify_time != iap_verify_data.verify_date.strftime("%Y%m%d%H%M%S"):
        return str.encode(ResultType.TOKEN_EXPIRE_ERROR)

    client_verify_date = datetime.strptime(client_token.verify_time, "%Y%m%d%H%M%S")

    remain_time = int((datetime.now() - client_verify_date).total_seconds())

    if remain_time > (60 * 60 * 24 * 5):
        str.encode(ResultType.TOKEN_EXPIRE_ERROR)

    # check hash code
    check_hash_code = generate_hash_code(APP_SECRET_KEY, iap_verify_data.udid,
                                         iap_verify_data.verify_date,
                                         iap_verify_data.transaction_id)

    if client_token.check_hash_code != check_hash_code.digest():
        return str.encode(ResultType.TOKEN_INVALID_ERROR)

    print('token verify : {0}'.format(ResultType.VERIFY_SUCCESS))
    return str.encode(ResultType.VERIFY_SUCCESS)