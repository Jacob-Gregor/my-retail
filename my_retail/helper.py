import redis
import ast

class Helper(object):
    def __init__(self):
        # Make self.url into environment variable
        self.last_write_failed = False
        # create seperate function for creating redis_py and make this funciton into get price or something
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
        #create seperate function for creating redis_py and make this funciton into get price or something
        redis_py = redis.StrictRedis(host='localhost', port=6379, db=0)
        try:
            result = redis_py.hget('product', id)
            return result
        except Exception:
            return 'something went wrong'

    def redis_update_pricing_info(self, redis_key, redis_field, name, values):
        """
        :param redis_key: Name of key the values will be put under
        :param redis_field: Name of field for each set of data
        :param name: Name data to be sent to redis(from external API)
        :param values: Price data to be sent to redis

        Take in data, how we want to format the data, and the key to reference this set
        of data and write it to Redis
        """
        # loops through list of datacenters and gives back each
        # datacenter dict (longName, name, id)

        # check if total is a dict
        if not isinstance(values, dict):
            raise TypeError("'total' must be of type (dictionary)")

        # remove unicode from values and set up data to go into redis
        new_value = {}
        currency_dict= {}
        currency_dict['currency_code'] = values['currency_code'].encode('ascii', 'ignore')
        currency_dict['value'] = values['value']
        new_value['name'] = name.encode('ascii', 'ignore')
        new_value['id'] = redis_field
        new_value['current_price'] = currency_dict
        try:
            self.redis_py.hset(redis_key, redis_field, new_value)
            print str(redis_key) + ' ' + str(redis_field) + ' ' + str(values)
        except Exception as e:
            return 'Redis failed to set data: %s' % e

    def format_data(self, this_id, data):
        # Make url into own function
        formatted_search = {}
        formatted_search['id'] = this_id
        formatted_search['current_price'] = self.redis_read_pricing_info(this_id)
        try:
            formatted_search['name'] = data['product']['item']['product_description']['title']
        except:
            return 'Failed to get data from url'
        return formatted_search