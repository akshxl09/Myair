from flask import *
from pymongo import MongoClient
from bson import json_util
import datetime
import os
import requests

list = Blueprint('list',__name__)

@list.route('/get_airpollution')
def get_airpollution():

    loc = request.args.get("loc")
    
    now = datetime.datetime.now()

    cur = MongoClient(os.environ['MYAIR_MONGODB'])
    db_name = 'Myair'
    col = cur[db_name]['airList']
    col_date = cur[db_name]['masterconfig']
    query = col.find_one()

    if not query:  #디비가 비어있으면
        url = 'http://openapi.seoul.go.kr:8088/' + os.environ['OPENDATA_APP_KEY'] +'/json/ListAirQualityByDistrictService/1/25/'
        data = requests.get(url).json()
        col.insert_many(data['ListAirQualityByDistrictService']['row'])
        col_date.insert_one({'airListDate': now})

    else:
        date = col_date.find_one({"airListDate":{'$exists': 'true'}})['airListDate']

        if (now - date).seconds/3600 >= 1: #디비에 넣은지 1시간이 지났으면
            url = 'http://openapi.seoul.go.kr:8088/' + os.environ['OPENDATA_APP_KEY'] +'/json/ListAirQualityByDistrictService/1/25/'
            data = requests.get(url).json()
            
            col.remove() #삭제가 좋을지, for문으로 하나씩 update가 좋을지
            col.insert_many(data['ListAirQualityByDistrictService']['row'])
            col_date.update_one({'airListDate':{'$exists': 'true'}}, {'$set':{'airListDate': now}})

    result = col.find_one({'MSRSTENAME': loc}) 

    return jsonify(
        result = 'success',
        data = json.loads(json_util.dumps(result))
    )