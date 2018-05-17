from flask import Flask, jsonify, redirect, request
from my_retail.helper import Helper
import urllib, json

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/products/'+str(0))

@app.route('/products/<int:id>', methods=['GET', 'PUT'])
def product(id):
    url = "http://redsky.target.com/v2/pdp/tcin/"+str(id)+"?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    helper = Helper()
    formatted_search = helper.format_data(id, data)
    return jsonify(formatted_search)


if __name__ == "main":
    app.run(debug=True)

