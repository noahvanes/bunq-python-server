import bunq_api as bunq
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

# Setup the Flask app
app = Flask(__name__)
api = Api(app)

# Accounts Resource
class Accounts(Resource):
    def get(self):
        all_accounts = bunq.all_accounts()
        return jsonify(list(all_accounts))
api.add_resource(Accounts, '/accounts')

# Account Resource
class Account(Resource):
    def get(self,id):
        account = bunq.get_account(id)
        return jsonify(account)
api.add_resource(Account, '/accounts/<id>')
