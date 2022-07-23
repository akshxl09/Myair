from flask import *
from pymongo import MongoClient
from bson import json_util
import datetime
import os

trans = Blueprint('trans',__name__)

@trans.route('/get_english_name')
def translation():

    loc = request.args.get("loc")

    cur = MongoClient(os.environ['MYAIR_MONGODB'])
    db_name = 'Myair'
    col = cur[db_name]['masterconfig']

    data = col.find_one({'key': 'region'})
    result = data['value']
    
    col = cur[db_name]['log']
    log_data = {
        'time': datetime.datetime.now(),
        'api': '/get_english_name',
        'ip': request.remote_addr,
        'parameter': None
    }
    col.insert_one(log_data)

    if(loc not in result):
        return jsonify(
            result = "failure",
            data = None
        )
    return jsonify(
        result = "success",
        data = json.loads(json_util.dumps(result[loc]))
    )