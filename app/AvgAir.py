from flask import *
from bson import json_util
import requests
from pymongo import MongoClient
import os
import datetime

avg = Blueprint('avg',__name__)

@avg.route('/get_avg_airpollution')
def avgAir():

    cur = MongoClient(os.environ['MYAIR_MONGODB'])
    db_name = 'Myair'
    col = cur[db_name]['avg']

    url = 'http://openapi.seoul.go.kr:8088/' + os.environ['OPENDATA_APP_KEY'] +'/json/ListAvgOfSeoulAirQualityService/1/1/'
    tmp = requests.get(url).json()
    data = tmp["ListAvgOfSeoulAirQualityService"]["row"][0]
    col.update({'GRADE': data['GRADE']}, data, upsert=True)
    
    col = cur[db_name]['log']
    log_data = {
        'time': datetime.datetime.now(),
        'api': '/get_avg_airpollution',
        'ip': request.remote_addr,
        'parameter': None
    }
    col.insert_one(log_data)

    return jsonify(
        result = 'success',
        data = json.loads(json_util.dumps(data))
    )
