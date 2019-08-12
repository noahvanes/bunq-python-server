from bunq_setup import BUNQ_CONF, TIME_CONF
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

### ACCOUNTS

# transform the bunq account representation into a JSON-friendly format
def account_to_json(account):
    return {
        'id': account.id_,
        'name': account.description,
        'balance': account.balance.value
    }

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
    account_json = account_to_json(account)
    return account_json

### CARDS

# helper
def card_primary_account(card):
    assignments = card.pin_code_assignment
    primary_assignment = next(ass for ass in assignments if ass.type_ == 'PRIMARY')
    return primary_assignment.monetary_account_id

# transform the bunq card representation into a JSON-friendly format
def card_to_json(card):
    return {
        'id': card.id_,
        'description': card.primary_account_numbers[0].description,
        'card_number': f'XXXX XXXX XXXX {card.primary_account_number_four_digit}',
        'expiry_date': card.expiry_date,
        'primary_account_id': card_primary_account(card)
    }

## !! HOTFIX to a bug in the bunq SDK

# Replace 'CardCredit' with 'CardDebit' in the response
def patchCreditCards(response_raw):
    data = response_raw._body_bytes.decode()
    patched_response_raw = data.replace('CardCredit','CardDebit')
    response_raw._body_bytes = bytes(patched_response_raw,'utf-8')

# Before converting the JSON, first patch the response data
class CardHotfix(endpoint.Card):
    @classmethod
    def _from_json_list(cls, response_raw, wrapper=None):
        patchCreditCards(response_raw)
        return endpoint.Card._from_json_list(response_raw,wrapper)
    @classmethod
    def _from_json(cls,response_raw,wrapper=None):
        patchCreditCards(response_raw)
        return endpoint.Card._from_json(response_raw,wrapper)

def all_cards():
    # ensure the session is still active
    refresh_api_context()
    # setup pagination
    pagination = bunqClient.Pagination()
    pagination.count = 10
    # make the request
    all_cards = CardHotfix.list(pagination.url_params_count_only).value
    # only include non-virtual, active cards
    non_virtual_cards = filter(lambda card: card.type_ != 'MASTERCARD_VIRTUAL', all_cards)
    all_active_cards = filter(lambda card: card.status == 'ACTIVE', non_virtual_cards)
    all_active_cards_json = map(card_to_json, all_active_cards)
    return all_active_cards_json

def get_card(id):
    # ensure the session is still active
    refresh_api_context()
    # get the card with the given id
    card = CardHotfix.get(id).value
    card_json = card_to_json(card)
    return card_json
