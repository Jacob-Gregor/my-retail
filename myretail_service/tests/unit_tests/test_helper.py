import unittest
import mock

from myretail_service.dev.helper import Helper


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

FAKE_REDIS_VALUES = (
    "{ 'current_price': { 'value': 2, 'currency_code': 'USD' },'name': 'test', 'id': 1}")

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

FORMATTED_RESULT_DB_NOT_SET = {
    'current_price': 'Not defined in DB',
    'name': 'test_title',
    'id': 2}


class TestHelper(unittest.TestCase):

    def test_product_exist_is_not_found(self):
        # Test valid hosts are added and invalid hosts are ignored.
        fake_helper = Helper()
        self.assertFalse(fake_helper.product_exist(FAKE_NOT_FOUND))

    def test_product_exist_is_found(self):
        # Test valid hosts are added and invalid hosts are ignored.
        fake_helper = Helper()
        self.assertTrue(fake_helper.product_exist(FAKE_FOUND))

    @mock.patch('redis.StrictRedis.hget')
    def test_redis_read_product_info(self, mock_hget):
        """Test happy path where hget is successful"""
        mock_hget.return_value = 5
        fake_helper = Helper()
        redis_result = fake_helper.redis_read_product_info(2)
        self.assertEqual(5, redis_result)

    @mock.patch('redis.StrictRedis.hget')
    def test_redis_read_product_return_error(self, mock_hget):
        """Test that exceptions is raised if hget fails"""
        mock_hget.side_effect = Exception('test error')
        fake_helper = Helper()
        result = fake_helper.redis_read_product_info(2)
        self.assertEqual('Error reading from Redis: test error', result)

    def test_redis_update_pricing_info_values_is_not_dict(self):
        """Test that TypeError is raised if values is not a dictionary"""
        fake_helper = Helper()
        with self.assertRaises(TypeError):
            fake_helper.redis_update_pricing_info('value', 'value', 'value', 2)

    @mock.patch('redis.StrictRedis.hset')
    def test_redis_update_pricing_info_values_update_data(self, mock_hset):
        """Test happy path. No exceptions"""
        fake_helper = Helper()
        fake_helper.redis_update_pricing_info('value', 'value', 'value', FAKE_VALUES)
        mock_hset.assert_called()

    @mock.patch('redis.StrictRedis.hset')
    def test_redis_update_pricing_info_values_raise_exception(self, mock_hset):
        """Test exception is raised if hset fails"""
        fake_helper = Helper()
        with self.assertRaises(Exception):
            mock_hset.side_effect = Exception
            fake_helper.redis_update_pricing_info('value', 'value', 'value', FAKE_VALUES)

    @mock.patch('myretail_service.dev.helper.Helper.redis_read_product_info')
    def test_format_data_redis_data_not_none(self, mock_read_redis):
        """Test that assertion is raised if redis connection fails"""
        fake_helper = Helper()
        mock_read_redis.return_value = FAKE_REDIS_VALUES
        result = fake_helper.format_data(2, FAKE_DATA)
        self.assertEqual(FORMATTED_RESULT, result)

    @mock.patch('myretail_service.dev.helper.Helper.redis_read_product_info')
    def test_format_data_redis_data_none(self, mock_read_redis):
        """Test that assertion is raised if redis connection fails"""
        fake_helper = Helper()
        mock_read_redis.return_value = None
        result = fake_helper.format_data(2, FAKE_DATA)
        self.assertEqual(FORMATTED_RESULT_DB_NOT_SET, result)
