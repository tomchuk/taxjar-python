import unittest
from mock import MagicMock, patch
import requests
import taxjar

class TestClient(unittest.TestCase):
    def setUp(self):
        self.api_key = 'heythere'
        self.api_url = taxjar.API_URL
        self.headers = {"Authorization": "Bearer heythere", "User-Agent": "TaxJarPython/1.1.2"}
        self.responder_mock = MagicMock()
        self.client = taxjar.Client(self.api_key, {}, self.responder_mock)

    def test_rates_for_location(self):
        action = lambda _: self.client.rates_for_location('90210')
        self.assert_request_occurred(action, 'get', 'rates/90210', {})

    def test_rates_for_location_with_deets(self):
        action = lambda _: self.client.rates_for_location('90210', {
            'city': 'Beverly Hills',
            'country': 'US'
        })
        self.assert_request_occurred(action, 'get', 'rates/90210', {
            'city': 'Beverly Hills',
            'country': 'US'
        })

    def test_categories(self):
        action = lambda _: self.client.categories()
        self.assert_request_occurred(action, 'get', 'categories', {})

    def test_tax_for_order(self):
        data = {'shipping': 0}
        action = lambda _: self.client.tax_for_order(data)
        self.assert_request_occurred(action, 'post', 'taxes', data)

    def test_list_orders(self):
        data = {'dummy': 'data'}
        action = lambda _: self.client.list_orders(data)
        self.assert_request_occurred(action, 'get', 'transactions/orders', data)

    def test_show_order(self):
        action = lambda _: self.client.show_order('1001')
        self.assert_request_occurred(action, 'get', 'transactions/orders/1001', {})

    def test_create_order(self):
        data = {'dummy': 'data'}
        action = lambda _: self.client.create_order(data)
        self.assert_request_occurred(action, 'post', 'transactions/orders', data)

    def test_update_order(self):
        data = {'dummy': 'data'}
        action = lambda _: self.client.update_order(1, data)
        self.assert_request_occurred(action, 'put', 'transactions/orders/1', data)

    def test_delete_order(self):
        action = lambda _: self.client.delete_order(1)
        self.assert_request_occurred(action, 'delete', 'transactions/orders/1', {})

    def test_list_refunds(self):
        data = {'from_transaction_date': '2016/01/01', 'to_transaction_date': '2017/01/01'}
        action = lambda _: self.client.list_refunds(data)
        self.assert_request_occurred(action, 'get', 'transactions/refunds', data)

    def test_show_refund(self):
        action = lambda _: self.client.show_refund('1001')
        self.assert_request_occurred(action, 'get', 'transactions/refunds/1001', {})

    def test_create_refund(self):
        data = {'dummy': 'data'}
        action = lambda _: self.client.create_refund(data)
        self.assert_request_occurred(action, 'post', 'transactions/refunds', data)

    def test_update_refund(self):
        data = {'dummy': 'data'}
        action = lambda _: self.client.update_refund(1, data)
        self.assert_request_occurred(action, 'put', 'transactions/refunds/1', data)

    def test_delete_refund(self):
        action = lambda _: self.client.delete_refund(1)
        self.assert_request_occurred(action, 'delete', 'transactions/refunds/1', {})

    def test_nexus_regions(self):
        action = lambda _: self.client.nexus_regions()
        self.assert_request_occurred(action, 'get', 'nexus/regions', {})

    def test_validate(self):
        action = lambda _: self.client.validate('1234')
        self.assert_request_occurred(action, 'get', 'validation', {'vat': '1234'})

    def test_summary_rates(self):
        action = lambda _: self.client.summary_rates()
        self.assert_request_occurred(action, 'get', 'summary_rates', {})

    def assert_request_occurred(self, action, request_method, uri, params):
        url = self.api_url + uri
        with patch.object(requests, request_method) as request_mock:
            action(0)
            request_mock.assert_called_with(
                url,
                headers=self.headers,
                **self._request_args(request_method, params)
            )
            self.responder_mock.assert_called_with(request_mock.return_value)

    def _request_args(self, method, params):
        args = {'timeout': 5}
        if method == 'get':
            args['params'] = params
        elif method == 'delete':
            pass
        else:
            args['json'] = params
        return args
