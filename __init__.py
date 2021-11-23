from app.index import index
from app.airList import list
from app.avgAir import avg
from flask import *
from flask_cors import CORS
from flask_jwt_extended import *
import os

from app.models.db.db_init import close_mongo_cur, init_models, open_mongo_cur
app=Flask(__name__)
CORS(app)

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = os.environ['MYAIR_JWT_KEY'],
    SECRET_KEY = os.environ['MYAIR_SECRET_KEY']
)

jwt = JWTManager(app)

def main():
    init_models()
    app.register_blueprint(index)
    app.register_blueprint(list)
    app.register_blueprint(avg)
    

@app.before_request
def before_request():
    open_mongo_cur()

@app.teardown_request
def teardown_request(exception):
    close_mongo_cur()

if __name__ == "__main__":
    main()
    app.run(debug=True)