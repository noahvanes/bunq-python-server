import bunq_api as bunq
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from flask_sslify import SSLify
from passlib.apps import custom_app_context as pwd_ctx
from bunq_setup import AUTH_CONF

# Setup the Flask app
app = Flask(__name__)
api = Api(app)
sslify = SSLify(app)

# setup authentication
auth = HTTPBasicAuth()
with open(AUTH_CONF,'r') as f:
    PWD_HASH = f.read()

@auth.verify_password
def verify_password(username,password):
    return pwd_ctx.verify(password,PWD_HASH)

# Accounts Resource
class Accounts(Resource):
    @auth.login_required
    def get(self):
        all_accounts = bunq.all_accounts()
        return jsonify(list(all_accounts))
api.add_resource(Accounts, '/accounts')

# Account Resource
class Account(Resource):
    @auth.login_required
    def get(self,id):
        account = bunq.get_account(id)
        return jsonify(account)
api.add_resource(Account, '/accounts/<id>')
