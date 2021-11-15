from flask import *

avg = Blueprint('avg',__name__)

@avg.route('/avg')
def avgAir():
    ...