import bunq_helper as bunq
from optparse import OptionParser
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

# Setup the Flask app
app = Flask(__name__)
api = Api(app)
        
# Accounts Resource
class Accounts(Resource):
        def get(self):
                all_accounts = bunq.all_accounts()
                return jsonify(list(map(lambda acc: {
                        'name': acc.description,
                        'balance': acc.balance.value
                }, all_accounts)))
api.add_resource(Accounts, '/accounts')

# First check if bunq is already configured
if bunq.bunq_is_configured():
        bunq.bunq_load_configuration()
else:
        parser = OptionParser()
        parser.add_option('--api-key',dest='apiKey',help='bunq api key (necessary if not yet configured)')
        options, args = parser.parse_args()
        bunq.bunq_new_configuration(options.apiKey)
# Then run the app
app.run(debug=True)