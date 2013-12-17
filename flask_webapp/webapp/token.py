__author__ = 'wes'
import hashlib


def create_token(result_type, app_secret_key, udid, verify_date, transaction_id):
    """ create sha1 token

    return data length format : result:4 +
                                token:20 +
                                udid_len:2 +
                                udid:udid_len +
                                verify_time:14 +
                                transaction_id_len:2
                                transaction_id:transaction_id_len

    """

    import struct

    check_hash_code = generate_hash_code(app_secret_key, udid, verify_date, transaction_id)

    token_format = '!4s20sH{0}s14s{1}s'.format(len(udid), len(transaction_id))
    final_data = struct.pack(token_format, str.encode(result_type), check_hash_code.digest(),
                             len(udid), str.encode(udid), str.encode(verify_date.strftime("%Y%m%d%H%M%S")),
                             str.encode(transaction_id))

    return final_data


def generate_hash_code(app_secret_key, udid, verify_date, transaction_id):
    verify_time = verify_date.strftime("%Y%m%d%H%M%S")
    check_origin_data = app_secret_key + udid + verify_time + transaction_id
    check_hash_code = hashlib.sha1(str.encode(check_origin_data))

    return check_hash_code


def decode_token(data):
    import collections

    token_data = collections.namedtuple('TokenData',
                                        ['check_hash_code', 'udid_len',
                                         'udid', 'verify_time', 'transaction_id'])

    client_check_hash_code = data[0:20]
    udid_len = int.from_bytes(data[20:22], byteorder="big")
    client_udid = str(data[22:(22 + udid_len)], 'utf-8')
    client_verify_time = str(data[(22 + udid_len):(22 + udid_len + 14)], 'utf-8')
    client_transaction_id = str(data[(22 + udid_len + 14):], 'utf-8')

    return token_data(client_check_hash_code,
                      udid_len,
                      client_udid,
                      client_verify_time,
                      client_transaction_id
    )