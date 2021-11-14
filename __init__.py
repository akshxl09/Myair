from flask import *
from flask_cors import CORS
from flask_jwt_extended import *
app=Flask(__name__)
CORS(app)

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "taebo",
    SECRET_KEY = "taebo"
)

jwt = JWTManager(app)

def main():
    init_db()


@app.before_request
def before_request():
    get_db()

@app.teardown_request
def teardown_request(exception):
    close_db()

if __name__ == "__main__":
    main()
    app.run(debug=True)