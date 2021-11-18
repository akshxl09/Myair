from flask import *
from pprint import pprint
import requests
from pymongo import MongoClient
import os

avg = Blueprint('avg',__name__)

@avg.route('/avg')
def avgAir():
    url = "http://openapi.seoul.go.kr:8088/6d704f6276616b7339367762736a70/json/ListAvgOfSeoulAirQualityService/1/5/"
    data = requests.get(url).json()
    pprint(data['ListAvgOfSeoulAirQualityService']['row'])

    cur = MongoClient(os.environ['MYAIR_MONGODB'])
    db_name = 'Myair'
    col_name = 'avg'
    
    # Create collection
    col = cur[db_name][col_name]
    col.insert_many(data['ListAvgOfSeoulAirQualityService']['row'])



    return redirect('/')