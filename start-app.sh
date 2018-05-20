#!/bin/bash

python setup.py install

export FLASK_APP=myretail_service/dev/main.py

flask run