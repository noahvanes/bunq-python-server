# Goal

The purpose of this project is to easily set up a webserver that is connected to your bunq account.
Currently, this webserver can then be queried to get the following information:

- an overview of all your bank accounts
- the details of a given bank account

The webserver uses a simple RESTful interface and server responses are given in JSON format.
This way, the idea is that the server can be reused as a common back-end for multiple applications and purposes.

# Usage

## Installation

Start by cloning this project on the server you wish to use and dive into the project folder.
Then, install the requirements of this project by running:
```
pip3 install -r requirements.txt
```
## Configuration

Before running the server, one needs to configure the webserver so that it is connected to your bunq account.
For this, you first need to run the following command:

```
python3 bunq_setup.py <api_key> <password> [--proxy-url <proxy>] [--description <description>] [--timezone <tz>] [--sandbox]
```

The parameter ``<api_key>`` is - non-suprisingly - an API key generated for the bunq account that you want to link to.
The parameter ``<password>`` is used to configure a password.
This is used to secure communication with the webserver (after all, we are working with sensitive data here): all requests are sent over HTTPS and need to include this password (using HTTP Basic Auth).

Finally, some optional arguments can be passed as well: 
- using ``--proxy-url``, you can specify a proxy server to use (default: no proxy server)
- using ``--description``, you can choose a name for the connection with your API key, which will be visible in the bunq app (default: hostname of the webserver)
- using ``--timezone``, you can set a timezone, which may be necessary (e.g., when the client and the webserver have different timezone configurations) to correctly report time on some server responses (default: Europe/Amsterdam)
- using ``--sandbox``, you can enable sandbox mode to test the webserver with a sandbox API key (default: disabled)

## Running the webserver

Once this configuration is done, the webserver can be launched :rocket:.
How this is done depends on the environment you are deploying in.
We refer to [the following documentation](https://flask.palletsprojects.com/en/1.0.x/deploying/#deployment) for detailed instructions.

Note that the webserver enforces the usage of HTTPS, so depending on your deployment environment, you may need to generate and/or provide an SSL certificate yourself first.

## Querying the server

Currently, the functionality of the webserver is limited and mainly designed around a single use-case: getting an overview of your accounts and their balance.
Therefore, the server only supports the following requests:
- ``GET /accounts``: to get an overview of all active accounts
- ``GET /accounts/<id>``: to get more detailed information (currently, just the description and balance) for the account with the given ``<id>``
- ``GET /accounts/<id>/numerics``: retrieves the balance for the account with the given ``<id>``, and outputs the data in the specific JSON-format that can be parsed by the [Numerics](https://cynapse.com/numerics/) app

Note that all requests need to be secured by providing the preconfigured password using HTTP Basic Auth (the username is ignored).

# More info

The webserver uses Python 3 and the [bunq Python SDK](https://github.com/bunq/sdk_python) to communicate with the bunq API.
