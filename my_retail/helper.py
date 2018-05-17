import redis

class Helper(object):
    def __init__(self):
        # Make self.url into environment variable
        self.last_write_failed = False
        self.url = "http://redsky.target.com/v2/pdp/tcin/" + str(
            id) + "?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics"

    def redis_read(self, id):
        #create seperate function for creating redis_py and make this funciton into get price or something
        redis_py = redis.StrictRedis(host='localhost', port=6379, db=0)
        try:
            result = redis_py.hget('product', id)
            return result
        except Exception as e:
            print e
            return 'something went wrong'

    def format_data(self, this_id, data):
        # Make url into own function
        formatted_search = {}
        formatted_search['id'] = this_id
        formatted_search['current_price'] = self.redis_read(this_id)
        try:
            formatted_search['name'] = data['product']['item']['product_description']['title']
        except:
            return 'Failed to get data from json'
        return formatted_search