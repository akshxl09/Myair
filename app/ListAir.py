from flask import *
from pprint import pprint
from pymongo import MongoClient
import os

import requests

list = Blueprint('list',__name__)

@list.route('/get_airpolution')
def get_airpolution():

    loc = request.args.get("loc")
#    print(loc)


    url = 'http://openapi.seoul.go.kr:8088/6d704f6276616b7339367762736a70/json/ListAirQualityByDistrictService/1/25/'
    data = requests.get(url).json()
#    pprint(data['ListAirQualityByDistrictService']['row'])

    cur = MongoClient(os.environ['MYAIR_MONGODB'])
    db_name = 'Myair'
    col_name = 'airpolution'
    
    # Create collection
    col = cur[db_name][col_name]
    #col.insert_many(data['ListAirQualityByDistrictService']['row'])

    i=0
    result = data['ListAirQualityByDistrictService']['row']
    while result[i]["MSRSTENAME"] != loc:
        i += 1               
    
    pprint(result[i])
    
    return jsonify(
        result = 'success',
        data = result[i]
    )