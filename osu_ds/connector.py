# coding=utf-8
import requests
from .errors import ConnectorException, InvalidParameter

__author__ = "DefaltSimon"


class OsuConnector:
    """
    Used to communicate with osu!api via requests.
    """
    def __init__(self, api_key):
        self.key = str(api_key)

    @staticmethod
    def validate(data):
        return dict((key, value) for key, value in data.items() if (key is not None and value is not None))

    def get(self, endpoint, payload):
        if type(payload) is not dict:
            raise InvalidParameter("payload was expected dict, got {}".format(type(payload).__name__))

        payload = self.validate(payload)

        # Automagically appends the api key if it was not done before
        if "k" not in payload.keys():
            payload["k"] = self.key

        resp = requests.get(
            url=endpoint,
            params=payload
        )

        if resp.status_code != 200:
            # Anything other than 200 is not good
            raise ConnectorException("Response code is {} {}".format(resp.status_code, resp.reason))

        # Converts to json format
        return resp.json()
