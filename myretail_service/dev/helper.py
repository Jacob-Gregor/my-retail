import redis


class Helper(object):
    def __init__(self):
        self.redis_py = redis.StrictRedis(host='localhost', port=6379, db=0)

    def product_exist(self, data):
        """
        :param data: JSON data retrieved from external API

        Determine if id provided by PUT request returned data
        """
        if 'available_to_promise_network' in data['product']:
            return True
        else:
            return False

    def redis_read_pricing_info(self, id):
        """
        :param id: id provided by GET response

        Read from Redis using id as the field in redis hget command
        """
        try:
            result = self.redis_py.hget('product', id)
            return result
        except Exception as e:
            return 'Error reading from Redis: %s' % e

    def redis_update_pricing_info(self, redis_key, redis_field, name, values):
        """
        :param redis_key: Name of key the values will be put under
        :param redis_field: Name of field for each set of data
        :param name: Name data to be sent to redis(from external API)
        :param values: Price data to be sent to redis

        Take in data, how we want to format the data, and the key to reference this set
        of data and write it to Redis
        """

        # check if total is a dict
        if not isinstance(values, dict):
            raise TypeError("'total' must be of type (dictionary)")

        # remove unicode from currency dictionary
        new_value = {}
        currency_dict = {}
        currency_dict['currency_code'] = values['currency_code'].encode('ascii', 'ignore')
        currency_dict['value'] = values['value']
        # add updated set of data to set in Redis
        new_value['name'] = name.encode('ascii', 'ignore')
        new_value['id'] = redis_field
        new_value['current_price'] = currency_dict
        try:
            self.redis_py.hset(redis_key, redis_field, new_value)
        except Exception as e:
            raise 'Redis failed to set data: %s' % e

    def format_data(self, product_id, data):
        """
       :param product_id: id of product
       :param data: data from external API

       Format data that contains the pricing info from Redis and all other data from external API
       """
        formatted_search = {}
        formatted_search['id'] = product_id
        formatted_search['current_price'] = self.redis_read_pricing_info(product_id)

        # Since we already checked if data exists, we do not need to do another check here
        formatted_search['name'] = data['product']['item']['product_description']['title']

        return formatted_search
