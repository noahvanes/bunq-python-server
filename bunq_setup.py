import socket
from argparse import ArgumentParser
import bunq.sdk.context as bunqContext

BUNQ_CONF = 'config/bunq.conf'
#PWD_CONF = 'data/pwd.txt'

def bunq_setup_configuration(api_key,description,proxy_url,production=True):
    env_type = bunqContext.ApiEnvironmentType.PRODUCTION if production else bunqContext.ApiEnvironmentType.SANDBOX
    api_context = bunqContext.ApiContext(env_type, api_key, description, proxy_url=proxy_url)
    api_context.save(BUNQ_CONF)

#def server_setup_password(pwd):
#    pass

if __name__ == '__main__':
    # parse the command-line arguments
    parser = ArgumentParser()
    parser.add_argument('api_key',help='the bunq API key to configure the server')
    #parser.add_argument('password',help='a password to secure the API requests')
    parser.add_argument('--proxy-url',dest='proxy_url',default=None,help='the proxy server to be used')
    parser.add_argument('--description',dest='description',default=socket.gethostname(),help='a description for the application')
    parser.add_argument('--sandbox',dest='production',action='store_false',help='use this flag to create a sandbox configuration')
    args = parser.parse_args()
    # setup the bunq API key
    bunq_setup_configuration(args.api_key,args.description,args.proxy_url,args.production)
    # setup the server password
    #server_setup_password(args.password)
