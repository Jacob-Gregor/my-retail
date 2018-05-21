# myRetail RESTful service
Technical Assessment Case Study # 1

Written in Python 2.7. Uses Flask for RESTful and Redis as a DB.

## Requirements for Use
  - This PoC is expected to be ran with Python 2.7.
  - The following is expected to be installed locally:
    - mock
    - flake8
    - tox
    - pytest-cov
    - redis
    - flask

  - Optional
     - redis-cli - installed locally for manually writing or reading data

## Setup
1. Clone this git repository

2. All dependencies need to be installed. myretail-service/install_dependencies.sh can be used to download
these dependencies (Note: install_dependencies.sh uses bash)

3. You will need two terminals to run this PoC.
  - One terminal will be needed to start a local redis server. To do this, just run the command `redis-server`
  - The other terminal will run flask. For this PoC we will be running flask locally. This can be accomplished two ways.
    - First by simply running `./start-app.sh` in the /myretail-service directory
    - Second manually running flask.
      - First define FLASK-APP: `FLASK_APP='myretail_service/dev.main.py`
      - Then run flask: `flask run`

## Interaction
  - ### HTTP GET Request
    There are two ways to interact with the PoC.
    - You can send a simple curl command: `curl localhost:8080/products/13860428`
    - Or you can browse the results through a web browser: `localhost:5000/products/13860428`

  - ### HTTP PUT Request
    - You can send a PUT request via curl: `curl localhost:5000/products/13860419 -X PUT -H "Content-Type: application/json" -d '{"current_price": {"currency_code": "USD", "value": 1244.69}, "id": 13860428, "name": "The Big Lebowski (Blu-ray)"}'`
    - Note: Any PUT request will either update the pricing information in Redis or it will add the data if it does not exist.


## Testing
  - There are two kinds of tests being done in this repo, unit tests and general format testing.
    To run either test, go in myretail-service/ and run `tox`. Running tox will run both types of test.

  - You can also have tox run just unit tests with `tox -e py27` and check the formatting with `tox -e pep8`.
