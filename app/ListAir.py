from flask import *
import json
from pprint import pprint


list = Blueprint('list',__name__)

@list.route('/list')
def listAir():
    with open('C:/Users/akshx/Desktop/vscode/Myair_JSON/listAir.json', 'r', encoding = "utf-8") as file:
        data = json.load(file)
    pprint(data)
    return redirect('/')