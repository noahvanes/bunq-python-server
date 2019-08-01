import bunq_api as bunq
from bunq_setup import AUTH_CONF, TIME_CONF, pwd_ctx
from math import floor
from pytz import timezone
from datetime import datetime
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from flask_sslify import SSLify

# Setup the Flask app
app = Flask(__name__)
api = Api(app)
sslify = SSLify(app)

# setup timezone settings
with open(TIME_CONF,'r') as f:
    TIME_ZONE = timezone(f.read())

# setup authentication
auth = HTTPBasicAuth()
with open(AUTH_CONF,'r') as f:
    PWD_HASH = f.read()

@auth.verify_password
def verify_password(username,password):
    # we ignore the username
    # instead, we only check if the password matches the one given at setup
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

# Account Resource
class AccountNumericsData(Resource):
    @auth.login_required
    def get(self,id):
        account = bunq.get_account(id)
        account_numerics = AccountNumericsData.account_to_numerics_json(account)
        return jsonify(account_numerics)
    @staticmethod
    def account_to_numerics_json(account):
        now = datetime.now().astimezone(TIME_ZONE)
        datestr = now.strftime("%d/%m")
        timestr = now.strftime("%H:%M")
        balance = floor(float(account['balance']))
        return {
            'postfix': f'Balance on {datestr} ({timestr})',
            'data': {
                'value': f'€{balance}'
            }
        }
api.add_resource(AccountNumericsData, '/accounts/<id>/numerics')

# only use this to test and debug your configuration locally
# assumes that you have an SSL certificate located in the config folder
# for production, it is recommended that you use e.g., gunicorn to launch this app
if __name__ == '__main__':
    ssl_context = ('config/cert.pem','config/key.pem')
    app.run(ssl_context=ssl_context)
