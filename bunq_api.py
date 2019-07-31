from bunq_setup import BUNQ_CONF
import bunq.sdk.client as bunqClient
import bunq.sdk.context as bunqContext
from bunq.sdk.model.generated import endpoint

# initialze the bunq API context on startup
BUNQ_CONTEXT = bunqContext.ApiContext.restore(BUNQ_CONF)
bunqContext.BunqContext.load_api_context(BUNQ_CONTEXT)

# when the sessions expires, need to reload
def refresh_api_context():
    if BUNQ_CONTEXT.ensure_session_active():
        BUNQ_CONTEXT.save(BUNQ_CONF)
        bunqContext.BunqContext.load_api_context(BUNQ_CONTEXT)

# get a list of all active accounts
def all_accounts():
    # ensure the session is still active
    refresh_api_context()
    # setup pagination
    pagination = bunqClient.Pagination()
    pagination.count = 25
    # make the request
    all_accounts = endpoint.MonetaryAccountBank.list(pagination.url_params_count_only).value
    # only include active accounts
    all_active_accounts = filter(lambda acc: acc.status == 'ACTIVE', all_accounts)
    all_active_accounts_json = map(account_to_json, all_active_accounts)
    return all_active_accounts_json

# get the balance of a specific account
def get_account(id):
    # ensure the session is still active
    refresh_api_context()
    # get the account with the given id
    account = endpoint.MonetaryAccountBank.get(id).value
    account_json = account_to_numerics_json(account)
    return account_json

# transform the bunq account representation into a JSON-friendly format
def account_to_json(account):
    return {
        'id': account.id_,
        'name': account.description,
        'balance': account.balance.value
    }

def account_to_numerics_json(account):
    return {
        'postfix': '',
        'data': {
            'value': f'€{account.balance.value}'
        }
    }
