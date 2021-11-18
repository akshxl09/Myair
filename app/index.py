from flask import *
import os

index = Blueprint('index',__name__)

@index.route('/')
def home():
    key = os.environ['KAKAO_APP_KEY']
    return render_template('index.html', appkey = key)