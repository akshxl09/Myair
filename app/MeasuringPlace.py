from flask import *

place = Blueprint('place',__name__)

@place.route('/place')
def measuringPlace():
    ...