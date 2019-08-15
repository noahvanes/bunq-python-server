import bunq_api as bunq
from bunq_setup import AUTH_CONF, TIME_CONF, pwd_ctx
from math import floor
from pytz import timezone
from datetime import datetime
from flask import Flask, jsonify, request
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

# Helper to convert a balance into the Numerics JSON format
def numerics_balance_json(amount):
    now = datetime.now().astimezone(TIME_ZONE)
    datestr = now.strftime("%d/%m")
    timestr = now.strftime("%H:%M")
    balance = floor(float(amount))
    return {
        'postfix': f'Balance on {datestr} ({timestr})',
        'data': {
            'value': f'€{balance}'
        }
    }

# Accounts Resource
class Accounts(Resource):
    @auth.login_required
    def get(self):
        is_joint = True if request.args.get('joint') == 'true' else False
        all_accounts = bunq.all_accounts(is_joint)
        return jsonify(list(all_accounts))
api.add_resource(Accounts, '/accounts')

# Account Resource
class Account(Resource):
    @auth.login_required
    def get(self,id):
        is_joint = True if request.args.get('joint') == 'true' else False
        account = bunq.get_account(id,is_joint)
        return jsonify(account)
api.add_resource(Account, '/accounts/<id>')

# Account Numerics Resource
class AccountNumericsData(Resource):
    @auth.login_required
    def get(self,id):
        is_joint = True if request.args.get('joint') == 'true' else False
        account = bunq.get_account(id,is_joint)
        account_balance = account['balance']
        account_numerics = numerics_balance_json(account_balance)
        return jsonify(account_numerics)
api.add_resource(AccountNumericsData, '/accounts/<id>/numerics')

# Cards Resource
class Cards(Resource):
    @auth.login_required
    def get(self):
        all_cards = bunq.all_cards()
        return jsonify(list(all_cards))
api.add_resource(Cards, '/cards')

# Card Resource
class Card(Resource):
    @auth.login_required
    def get(self,id):
        card = bunq.get_card(id)
        return jsonify(card)
api.add_resource(Card,'/cards/<id>')

# Card Numerics Resource
class CardNumericsData(Resource):
    @auth.login_required
    def get(self,id):
        card = bunq.get_card(id)
        account_id = card['primary_account_id']
        account = bunq.get_account(account_id)
        account_balance = account['balance']
        account_numerics = numerics_balance_json(account_balance)
        return jsonify(account_numerics)
api.add_resource(CardNumericsData,'/cards/<id>/numerics')
