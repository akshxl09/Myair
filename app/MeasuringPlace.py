from flask import *
from pprint import pprint
from flask.helpers import total_seconds
import requests
from pymongo import MongoClient
import os

place = Blueprint('place',__name__)

@place.route('/place')
def measuringPlace():
    url = "http://openapi.seoul.go.kr:8088/6d704f6276616b7339367762736a70/json/SearchMeasuringSTNOfAirQualityService/1/25/"
    data = requests.get(url).json()
    pprint(data['SearchMeasuringSTNOfAirQualityService']['row'])

    cur = MongoClient(os.environ['MYAIR_MONGODB'])
    db_name = 'Myair'
    col_name = 'place'
    
    # Create collection
    col = cur[db_name][col_name]
    col.insert_many(data['SearchMeasuringSTNOfAirQualityService']['row'])


    return redirect('/')