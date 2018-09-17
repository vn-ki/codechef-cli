import requests
import logging
from codechef_cli.data import Data
import codechef_cli.exceptions as exceptions

logger = logging.getLogger(__name__)
API_URL = 'https://api.codechef.com'


def call_api(*path, params=None, method=None):
    # TODO:adapt this for method=POST
    if "tokens" not in Data.keys():
        raise exceptions.TokensNotFound
    tokens = Data["tokens"]
    # set apporipriate headers
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(tokens['access_token'])
    }
    # buid complete path from pieces `path`
    compiled_path = "/".join([str(part) for part in path])

    url = "{}/{}".format(API_URL, compiled_path)

    logger.debug("calling {}, params: {}".format(url, params))
    response = requests.get(url, headers=headers, params=params)
    response_map = response.json()
    logger.debug("response from CC: {}".format(response_map))

    if response_map['status'] == "OK":
        return response_map["result"]["data"]["content"]
    else:
        logger.debug("status not OK, result: {}".format(
            response_map["result"]))
        try:
            # check if error is unauthorized
            if response_map["result"]["errors"][0]["code"] == "unauthorized":
                logger.debug("tokens expired, trying to refresh tokens")
                from codechef_cli.config import Config
                global_config = Config["global"]
                resp = requests.post("{}/oauth/token".format(API_URL),
                                     json={"grant_type": "refresh_token",
                                           "refresh_token": tokens["refresh_token"],
                                           "client_id": global_config["client_id"],
                                           "client_secret": global_config["client_secret"]
                                           },
                                     headers={'content-Type': 'application/json'})
                resp_map = resp.json()
                logger.debug("response from CC: ", resp_map)
                # store tokens
                if resp_map["status"] == "OK":
                    Data["tokens"] = resp_map["result"]["data"]
                    # re-run the query
                    logger.debug("retrying query with new tokens")
                    return call_api(*path, params=params, method=method)
                else:
                    # TODO:seperate exception?
                    raise exceptions.CodechefException
            else:
                err = response_map['result']['errors'][0]
                raise exceptions.APIError('Message: {}, Code: {}'.format(err['message'], err['code']))
        # TODO: handle exceptions carefully
        except Exception as e:
            raise


def get_data(*path, params=None):
    return call_api(*path, params=params, method="GET")
