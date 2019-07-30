import socket
from argparse import ArgumentParser
import bunq.sdk.context as bunqContext

BUNQ_CONF = 'bunq.conf'

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_argument('--api-key',dest='api_key',help='the bunq API key to configure the server')
    args = parser.parse_args()
    bunq_setup_configuration(api_key)

def bunq_setup_configuration(api_key):
    env_type = bunqContext.ApiEnvironmentType.PRODUCTION
    description = socket.gethostname()
    api_context = bunqContext.ApiContext(env_type, api_key, description)
    api_context.save(BUNQ_CONF)