import socket
import os.path
import bunq.sdk.client as bunqClient
import bunq.sdk.context as bunqContext
from bunq.sdk.model.generated import endpoint

BUNQ_CONF = "bunq.conf"
BUNQ_CONTEXT = None

def bunq_is_configured():
        return os.path.exists(BUNQ_CONF)

def bunq_new_configuration(api_key):
        global BUNQ_CONTEXT
        env_type = bunqContext.ApiEnvironmentType.PRODUCTION
        description = socket.gethostname()
        BUNQ_CONTEXT = bunqContext.ApiContext(env_type, api_key, description)
        BUNQ_CONTEXT.save(BUNQ_CONF)
        bunqContext.BunqContext.load_api_context(BUNQ_CONTEXT)

def bunq_load_configuration():
        global BUNQ_CONTEXT
        BUNQ_CONTEXT = bunqContext.ApiContext.restore(BUNQ_CONF)
        bunqContext.BunqContext.load_api_context(BUNQ_CONTEXT)

def refresh_api_context():
        if BUNQ_CONTEXT.ensure_session_active():
               BUNQ_CONTEXT.save(BUNQ_CONF)
               bunqContext.BunqContext.load_api_context(BUNQ_CONTEXT)

def all_accounts():
        # ensure the seesion is still active
        refresh_api_context()
        # setup pagination
        pagination = bunqClient.Pagination()
        pagination.count = 25
        # make the request
        all_accounts = endpoint.MonetaryAccountBank.list(pagination.url_params_count_only).value
        return all_accounts

def print_all_accounts():
        #print(f"Found active account {account.description} with balance €{account.balance.value}")
        pass