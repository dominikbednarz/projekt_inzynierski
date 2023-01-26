from flask import Flask, request # pip install Flask
from flask_httpauth import HTTPBasicAuth # pip install Flask-HTTPAuth
from werkzeug.security import generate_password_hash, check_password_hash
from kafka_utils import produce, consume
import json


app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("test1234")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/produce', methods=['POST'])
@auth.login_required
def api_produce():
  ans = produce(request.get_json())
  print(ans)
  return '', 204

@app.route('/consume', methods=['POST'])
@auth.login_required
def api_consume():
  data=consume(request.get_json())
  response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
  return response
