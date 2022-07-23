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

    now = datetime.datetime.now().strftime("%Y%m%d%H00")
    cur = MongoClient(os.environ['MYAIR_MONGODB'])
    db_name = 'Myair'
    col = cur[db_name]['airList']
    query = col.find_one({'date': now})

    if not query:  #현재 시간에 대한 db가 비어있으면
        url = 'http://openapi.seoul.go.kr:8088/' + os.environ['OPENDATA_APP_KEY'] +'/json/ListAirQualityByDistrictService/1/25/'
        tmp = requests.get(url).json()
        data = tmp["ListAirQualityByDistrictService"]["row"]

        if data[0]["MSRDATE"] == now: #호출한 api에 현재 시간에 해당하는 정보가 있을 경우         
            doc = {}
            doc['date'] = now
            for row in data:
                temp = {'GRADE': row['GRADE'],
                'POLLUTANT': row['POLLUTANT'],
                'CARBON': row['CARBON'],
                'NITROGEN': row['NITROGEN'],
                'OZONE': row['OZONE'],
                'SULFUROUS': row['SULFUROUS'],
                'PM10': row['PM10'],
                'PM25': row['PM25']
                }
                doc[row['MSRSTENAME']] = temp

            col.insert_one(doc)
            query = col.find_one({'date': now})

        else: #호출한 api에도 현재 시간에 해당하는 정보 없을 경우
            query = col.find().sort("date", -1).limit(1)[0]

    col = cur[db_name]['log']
    log_data = {
        'time': datetime.datetime.now(),
        'api': '/get_airpollution',
        'ip': request.remote_addr,
        'parameter': None
    }
    col.insert_one(log_data)

    if(loc not in query):
        return jsonify(
            result = "failure",
            data = None
        )
    return jsonify(
        result = 'success',
        data = json.loads(json_util.dumps(query[loc]))
    )