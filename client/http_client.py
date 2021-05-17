import requests
import logging

logger = logging.getLogger(__name__)


def get_key(url, key: str) -> dict:
    """Retreive key from server

    Raises exceptions in case of HTTP error

    :params url: http api endpoint to make calls to
    :params key: query parameter for the key resource
    :returns :str: value retreived from the server for the corresponding key
    """
    try:
        resp = requests.get(url, params={"key": key})
        resp.raise_for_status()
        if resp.status_code == requests.codes.ok:
            resp_dict = resp.json()
            return resp_dict
    except Exception as err:
        logger.debug(err)
        logging.error("Unable to process the request")


def put_key(url, key: str, value: str) -> None:
    """Update key value in the server

    :params url: http api endpoint to make calls to
    :params key: query parameter for the key resource
    :params value: query parameter for the value resource
    :returns :None:
    """
    try:
        resp = requests.put(url, params={"key": key, "value": value})
        resp.raise_for_status()
    except Exception as err:
        logger.debug(err)
        logging.error("Unable to process the request")
