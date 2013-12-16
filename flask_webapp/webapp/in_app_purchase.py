import urllib
import base64
from flask import request, Blueprint, current_app, json, jsonify


iap = Blueprint('iap', __name__, template_folder='templates')

SAND_BOX_VERIFY_URL = "https://sandbox.itunes.apple.com/verifyReceipt"
PRODUCTION_VERIFY_URL = "https://buy.itunes.apple.com/verifyReceipt"
APP_SECRET_KEY = '123456789'


class ResultType:
    VERIFY_SUCCESS = 'succ'
    VERIFY_FAIL = 'fail'


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
        iap_verify_data = _backup_verify_data(verify_result)

        return _create_token(APP_SECRET_KEY, udid, iap_verify_data.verify_date, iap_verify_data.transaction_id)
    else:
        return str.encode(ResultType.VERIFY_FAIL)


def _is_ios6(receipt_data):
    if 'original_transaction_id' in receipt_data:
        return True

    else:
        return False


def _backup_verify_data(verify_result):
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
            iap_verify_data = IAPVerifyData.create_for_ios6('ooo', verify_result['receipt'])
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
            iap_verify_data = IAPVerifyData.create_for_ios7('ooo',
                                                            verify_result['receipt']['bundle_id'],
                                                            verify_result['receipt']['application_version'],
                                                            in_app_result)
            iap_verify_data.save()

    return iap_verify_data


def _create_token(app_secret_key, udid, verify_date, transaction_id):
    """ create sha1 token

    return data length format : result:4 +
                                token:20 +
                                udid_len:2 +
                                udid:udid_len +
                                verify_time:14 +
                                transaction_id_len:2
                                transaction_id:transaction_id_len

    """

    import hashlib
    import struct

    verify_time = verify_date.strftime("%Y%m%d%H%M%S")
    check_origin_data = app_secret_key + udid + verify_time + transaction_id
    check_hash_code = hashlib.sha1(str.encode(check_origin_data))

    token_format = '!4s20sH{0}s14s{1}s'.format(len(udid), len(transaction_id))
    final_data = struct.pack(token_format, str.encode(ResultType.VERIFY_SUCCESS), check_hash_code.digest(),
                             len(udid), str.encode(udid), str.encode(verify_time), str.encode(transaction_id))

    return final_data


@iap.route('/token/verify', methods=['POST', 'GET'])
def iap_token_verify():
    """ iap token verify """

    check_hash_code = request.data[0:20]
    udid_len = int.from_bytes(request.data[20:22], byteorder="big")
    udid = str(request.data[22:(22 + udid_len)], 'utf-8')
    verify_time = str(request.data[(22 + udid_len):(22 + udid_len + 14)], 'utf-8')
    transaction_id = str(request.data[(22 + udid_len + 14):], 'utf-8')

    return str.encode(ResultType.VERIFY_SUCCESS)