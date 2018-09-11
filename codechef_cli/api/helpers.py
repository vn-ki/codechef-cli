import requests
import logging
from codechef_cli.data import Data
import codechef_cli.exceptions

logger = logging.getLogger(__name__)
API_URL = 'https://api.codechef.com'


def call_api(*path, params=None, method=None):
    #TODO:adapt this for method=POST
    tokens = Data["tokens"]
    # set apporipriate headers
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(tokens['access_token'])
    }
    # buid complete path from pieces `path`
    path = "/".join([str(part) for part in path])
    if isinstance(params, dict):
        query = "&".join(["{}={}".format(key, params[key])
                          for key in params.keys()])
    else:
        query = ""

    url = "{}/{}?{}".format(API_URL, path, query)

    logger.debug("calling {}".format(url))
    response = requests.get(url, headers=headers)
    response_map = response.json()
    logger.debug("response from CC:status: {}".format(response_map['status']))

    if response_map['status'] == "OK":
        return response_map["result"]["data"]["content"]
    else:
        #TODO:check response_map["result"] for error and refresh tokens accordingly
        raise exceptions.APIInputError

def get_data(*path, params=None):
    call_api(*path, params=params, method="GET")
