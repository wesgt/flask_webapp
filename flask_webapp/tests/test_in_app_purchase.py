import unittest
from flask import json
import webapp
from webapp.in_app_purchase import ResultType, iap


class IAPTestCase(unittest.TestCase):

    def setUp(self):
        app = webapp.create_app('config/config_testing.cfg')
        app.config['TESTING'] = True
        app.register_blueprint(iap, url_prefix='/mobile/iap')
        self.client = app.test_client()

    def tearDown(self):
        from webapp.database import db_session, drop_all_table

        if db_session:
            db_session.remove()

        drop_all_table()
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_iap_receipts_verify_return_correct(self):
        receipt_data = 'eyJzaWduYXR1cmUiID0gIkFrSEkxZkxOV3V2bkV2Z1hoeVRmaHVDQjVnNnFvTWQvVXVUK0VkblA4bi9yL0QrZjZsZnlockhJbjZFVVlnckpJY0h1UUd4TE9TS3lVNURSVHNkazRScnBBTnlhYWY4NmdFK3dQRzFQM01WRU92MzhvMHFSUmhUcHIyc1FZYlFNS0t4QzQzemxzV3dGZzdYdXNlR2xqNHhFY3FnVzhFbjhuR29iVWtLL3NOZTBBQUFEVnpDQ0ExTXdnZ0k3b0FNQ0FRSUNDR1VVa1UzWldBUzFNQTBHQ1NxR1NJYjNEUUVCQlFVQU1IOHhDekFKQmdOVkJBWVRBbFZUTVJNd0VRWURWUVFLREFwQmNIQnNaU0JKYm1NdU1TWXdKQVlEVlFRTERCMUJjSEJzWlNCRFpYSjBhV1pwWTJGMGFXOXVJRUYxZEdodmNtbDBlVEV6TURFR0ExVUVBd3dxUVhCd2JHVWdhVlIxYm1WeklGTjBiM0psSUVObGNuUnBabWxqWVhScGIyNGdRWFYwYUc5eWFYUjVNQjRYRFRBNU1EWXhOVEl5TURVMU5sb1hEVEUwTURZeE5ESXlNRFUxTmxvd1pERWpNQ0VHQTFVRUF3d2FVSFZ5WTJoaGMyVlNaV05sYVhCMFEyVnlkR2xtYVdOaGRHVXhHekFaQmdOVkJBc01Fa0Z3Y0d4bElHbFVkVzVsY3lCVGRHOXlaVEVUTUJFR0ExVUVDZ3dLUVhCd2JHVWdTVzVqTGpFTE1Ba0dBMVVFQmhNQ1ZWTXdnWjh3RFFZSktvWklodmNOQVFFQkJRQURnWTBBTUlHSkFvR0JBTXJSakYyY3Q0SXJTZGlUQ2hhSTBnOHB3di9jbUhzOHAvUndWL3J0LzkxWEtWaE5sNFhJQmltS2pRUU5mZ0hzRHM2eWp1KytEcktKRTd1S3NwaE1kZEtZZkZFNXJHWHNBZEJFakJ3Ukl4ZXhUZXZ4M0hMRUZHQXQxbW9LeDUwOWRoeHRpSWREZ0p2MllhVnM0OUIwdUp2TmR5NlNNcU5OTEhzREx6RFM5b1pIQWdNQkFBR2pjakJ3TUF3R0ExVWRFd0VCL3dRQ01BQXdId1lEVlIwakJCZ3dGb0FVTmgzbzRwMkMwZ0VZdFRKckR0ZERDNUZZUXpvd0RnWURWUjBQQVFIL0JBUURBZ2VBTUIwR0ExVWREZ1FXQkJTcGc0UHlHVWpGUGhKWENCVE16YU4rbVY4azlUQVFCZ29xaGtpRzkyTmtCZ1VCQkFJRkFEQU5CZ2txaGtpRzl3MEJBUVVGQUFPQ0FRRUFFYVNiUGp0bU40Qy9JQjNRRXBLMzJSeGFjQ0RYZFZYQWVWUmVTNUZhWnhjK3Q4OHBRUDkzQmlBeHZkVy8zZVRTTUdZNUZiZUFZTDNldHFQNWdtOHdyRm9qWDBpa3lWUlN0USsvQVEwS0VqdHFCMDdrTHM5UVVlOGN6UjhVR2ZkTTFFdW1WL1VndkRkNE53Tll4TFFNZzRXVFFmZ2tRUVZ5OEdYWndWSGdiRS9VQzZZNzA1M3BHWEJrNTFOUE0zd294aGQzZ1NSTHZYaitsb0hzU3RjVEVxZTlwQkRwbUc1K3NrNHR3K0dLM0dNZUVONS8rZTFRVDlucC9LbDFuaithQnc3QzB4c3kwYkZuYUFkMWNTUzZ4ZG9yeS9DVXZNNmd0S3Ntbk9PZHFUZXNicDBiczhzbjZXcXMwQzlkZ2N4Ukh1T01aMnRtOG5wTFVtN2FyZ09TelE9PSI7InB1cmNoYXNlLWluZm8iID0gImV3b0pJbTl5YVdkcGJtRnNMWEIxY21Ob1lYTmxMV1JoZEdVdGNITjBJaUE5SUNJeU1ERXpMVEExTFRBNUlESXdPak0xT2pBeElFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW5WdWFYRjFaUzFwWkdWdWRHbG1hV1Z5SWlBOUlDSmtNV1ZoWmpRNFpEVmxOakJqTmpreFlUZzJZVE14TURoallXWTNPVEF4TjJZME16bGtZV1kxSWpzS0NTSnZjbWxuYVc1aGJDMTBjbUZ1YzJGamRHbHZiaTFwWkNJZ1BTQWlNVEF3TURBd01EQTNNelUzTWpZNU5TSTdDZ2tpWW5aeWN5SWdQU0FpTVM0d0lqc0tDU0owY21GdWMyRmpkR2x2YmkxcFpDSWdQU0FpTVRBd01EQXdNREEzTXpVM01qWTVOU0k3Q2draWNYVmhiblJwZEhraUlEMGdJakVpT3dvSkltOXlhV2RwYm1Gc0xYQjFjbU5vWVhObExXUmhkR1V0YlhNaUlEMGdJakV6TmpneE5UWTVNREV5TlRraU93b0pJblZ1YVhGMVpTMTJaVzVrYjNJdGFXUmxiblJwWm1sbGNpSWdQU0FpT1RFNE5EY3pNakV0UlVRME1TMDBNMEZCTFRrd1FUUXRPVVUxTjBVMlJFWXdSa0k0SWpzS0NTSndjbTlrZFdOMExXbGtJaUE5SUNKVGQyOXlaREF3TVNJN0Nna2lhWFJsYlMxcFpDSWdQU0FpTmpRek5URXpNamt5SWpzS0NTSmlhV1FpSUQwZ0ltTnZiUzV6YjJaMGMzUmhjaTUwWlhOMFUzZGtabWxuYUhRaU93b0pJbkIxY21Ob1lYTmxMV1JoZEdVdGJYTWlJRDBnSWpFek5qZ3hOVFk1TURFeU5Ua2lPd29KSW5CMWNtTm9ZWE5sTFdSaGRHVWlJRDBnSWpJd01UTXRNRFV0TVRBZ01ETTZNelU2TURFZ1JYUmpMMGROVkNJN0Nna2ljSFZ5WTJoaGMyVXRaR0YwWlMxd2MzUWlJRDBnSWpJd01UTXRNRFV0TURrZ01qQTZNelU2TURFZ1FXMWxjbWxqWVM5TWIzTmZRVzVuWld4bGN5STdDZ2tpYjNKcFoybHVZV3d0Y0hWeVkyaGhjMlV0WkdGMFpTSWdQU0FpTWpBeE15MHdOUzB4TUNBd016b3pOVG93TVNCRmRHTXZSMDFVSWpzS2ZRPT0iOyJlbnZpcm9ubWVudCIgPSAiU2FuZGJveCI7InBvZCIgPSAiMTAwIjsic2lnbmluZy1zdGF0dXMiID0gIjAiO30='
        verify_rv = self.client.post(
            '/mobile/iap/receipts/verify',
            data=dict(user_id='1234', receipt_data=receipt_data),
            follow_redirects=False)

        verify_result = json.loads(str(verify_rv.data, 'utf-8'))
        self.assertEqual(ResultType.VERIFY_SUCCESS, verify_result['result'])

    def test_iap_receipts_verify_return_error(self):
        verify_rv = self.client.post(
            '/mobile/iap/receipts/verify',
            data=dict(user_id='1234', receipt_data=''),
            follow_redirects=False)

        verify_result = json.loads(str(verify_rv.data, 'utf-8'))
        self.assertEqual(ResultType.VERIFY_FAIL, verify_result['result'])
