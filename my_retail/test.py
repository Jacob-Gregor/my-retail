import redis
redis_py = redis.StrictRedis(host='localhost', port=6379, db=0)




def write_to_redis(redis_key, redis_field, values):
    """
    :param redis_key: Name of key the values will be put under
    :param redis_field: Name of field for each set of data
    :param values: Data to be sent to redis

    Take in data, how we want to format the data, and the key to reference this set
    of data and write it to Redis
    """
    # loops through list of datacenters and gives back each
    # datacenter dict (longName, name, id)

    # check if totals is a list of dicts
    if not isinstance(values, list):
        raise TypeError("'totals' must be of type (list)")


    for value in values:
        temp_id = value[redis_field]
        del value[redis_field]

        # check if total is a dict
        if not isinstance(value, dict):
            raise TypeError("'total' must be of type (dictionary)")
        try:
            # https://redis-py.readthedocs.io/en/latest/#redis.StrictRedis
            redis_py.hset(redis_key, temp_id, value)
            print str(redis_key) + ' ' + str(temp_id) + ' ' + str(value)
        except Exception as e:
            return 'redis failed to set data.'

product_list = []

product1 = {}
product1['id'] = int(13860438)
product1['value'] = float(13.49)
product1['currency_code'] = 'USD'
product_list.append(product1)

product2 = {}
product2['id'] = int(13860439)
product2['value'] = float(15.00)
product2['currency_code'] = 'USD'
product_list.append(product2)

product3 = {}
product3['id'] = int(13860424)
product3['value'] = float(11.23)
product3['currency_code'] = 'USD'
product_list.append(product3)

print len(product_list)
for thing in product_list:
    print thing
write_to_redis('product', 'id', product_list)

