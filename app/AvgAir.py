from flask import *
from bson import json_util
import datetime
import requests
from pymongo import MongoClient
import os

avg = Blueprint('avg',__name__)

@avg.route('/get_avg_airpollution')
def avgAir():

    now = datetime.datetime.now()

    cur = MongoClient(os.environ['MYAIR_MONGODB'])
    db_name = 'Myair'
    col = cur[db_name]['avg']
    col_date = cur[db_name]['masterconfig']
    query = col.find_one()

    if not query:  #디비가 비어있으면
        url = 'http://openapi.seoul.go.kr:8088/' + os.environ['OPENDATA_APP_KEY'] +'/json/ListAvgOfSeoulAirQualityService/1/1/'
        data = requests.get(url).json()
        col.insert_one(data['ListAvgOfSeoulAirQualityService']['row'][0])
        col_date.insert_one({'avgDate': now})

    else:
        date = col_date.find_one({"avgDate":{'$exists': 'true'}})['avgDate']

        if (now - date).seconds/3600 >= 1: #디비에 넣은지 1시간이 지났으면
            url = 'http://openapi.seoul.go.kr:8088/' + os.environ['OPENDATA_APP_KEY'] +'/json/ListAvgOfSeoulAirQualityService/1/1/'
            data = requests.get(url).json()
            
            col.remove()
            col.insert_one(data['ListAvgOfSeoulAirQualityService']['row'][0])
            col_date.update_one({'avgDate':{'$exists': 'true'}}, {'$set':{'avgDate': now}})

    result = col.find_one()

    return jsonify(
        result = 'success',
        data = json.loads(json_util.dumps(result))
    )
