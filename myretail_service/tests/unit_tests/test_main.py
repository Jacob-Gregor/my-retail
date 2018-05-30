import unittest
import json
import mock

from myretail_service.dev.main import app

FAKE_NOT_FOUND = {
    'product': {
        'item:': {

        }
    }
}

FAKE_FOUND = {
    'product': {
        'item:': {
            },
        'available_to_promise_network': {
        }
    }
}

FAKE_VALUES = {
    'value': 2,
    'currency_code': 'USD'
}

FAKE_DATA = {
    'product': {
        'item': {
            'product_description': {
                "title": 'test_title'
            }
        }
    }
}

FORMATTED_RESULT = {
    'current_price': {
            'currency_code': 'USD',
            'value': 2
        },
    'name': 'test_title',
    'id': 2}


class TestDataManagement(unittest.TestCase):
    def setUp(self):
        # Set up test app client
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.put_data = {
            "current_price": {
                "currency_code": "USD",
                "value": 2
            },
            "id": 13860419,
            "name": "test"
        }

    @mock.patch('myretail_service.dev.helper.Helper.product_exist')
    @mock.patch('myretail_service.dev.helper.Helper.redis_read_product_info')
    @mock.patch('myretail_service.dev.helper.Helper.format_data')
    def test_product_get(self, mock_format, mock_redis_read, mock_product_exist):
        # Test HTTP GET
        mock_redis_read.return_value = FAKE_VALUES
        mock_format.return_value = FORMATTED_RESULT
        mock_product_exist.return_value = True
        response = self.client.get('/products/13860428')
        self.assertNotEqual('Product does not exist.', response.data)

    @mock.patch('myretail_service.dev.helper.Helper.product_exist')
    @mock.patch('myretail_service.dev.helper.Helper.redis_update_pricing_info')
    @mock.patch('myretail_service.dev.helper.Helper.format_data')
    def test_product_put(self, mock_format, mock_redis_update, mock_product_exist):
        # Test HTTP PUT.
        mock_format.return_value = FORMATTED_RESULT
        mock_product_exist.return_value = True
        response = self.client.put('/products/13860428', data=json.dumps(self.put_data),
                                   headers={'Content-Type': 'application/json'})
        self.assertNotEqual('Product not found.', response.data)

    @mock.patch('myretail_service.dev.helper.Helper.product_exist')
    @mock.patch('myretail_service.dev.helper.Helper.redis_read_product_info')
    @mock.patch('myretail_service.dev.helper.Helper.format_data')
    def test_product_else(self, mock_format, mock_redis_read, mock_product_exist):
        # Check that product returns general messsage if external api does not contain provided ID
        mock_redis_read.return_value = FAKE_VALUES
        mock_format.return_value = FORMATTED_RESULT
        mock_product_exist.return_value = False
        result = self.client.get('/products/13860428')
        self.assertEqual('Product not found.', result.data)

    def test_index(self):
        # Test redirection occurs
        response = self.client.get('/')
        self.assertNotEqual('Product not found.', response.data)
