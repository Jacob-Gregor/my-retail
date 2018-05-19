from flask import Flask, jsonify, redirect, request
from my_retail.helper import Helper
import urllib, json

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/products/'+str(0))

@app.route('/products/<int:id>', methods=['GET', 'PUT'])
def product(id):
    helper = Helper()
    url = "http://redsky.target.com/v2/pdp/tcin/" + str(
        id) + "?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    if request.method == 'GET' and helper.product_exist(data):
        formatted_search = helper.format_data(id, data)
        return jsonify(formatted_search)
    elif request.method == 'PUT' and helper.product_exist(data):
        # Add an else statement if ID does exist on URL

        thing = request.get_json()
        helper.redis_update_pricing_info('product', id,
                                         data['product']['item']['product_description']['title'],
                                         thing['current_price'])

        print thing['current_price']['currency_code'].encode('ascii', 'ignore')
        return 'something'
    else:
        return 'Product does not exist.'

if __name__ == "main":
    app.run(debug=True)

