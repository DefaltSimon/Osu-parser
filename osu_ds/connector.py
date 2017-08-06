# coding=utf-8
import aiohttp

try:
    from ujson import loads
except ImportError:
    from json import loads

from .errors import ConnectorException, InvalidParameter

__author__ = "DefaltSimon"


class OsuConnector:
    """
    Used to communicate with osu!api via requests.
    """
    def __init__(self, api_key):
        self.key = str(api_key)

        self.session = None

    def _handle_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(json_serialize=loads)

        return self.session

    @staticmethod
    def _build_url(url, **fields):
        if not url.endswith("?"):
            url += "?"

        field_list = ["{}={}".format(key, value) for key, value in fields.items()]
        return str(url) + "&".join(field_list)

    @staticmethod
    def validate(data):
        return dict((key, value) for key, value in data.items() if (key is not None and value is not None))

    async def get(self, endpoint, payload):
        if type(payload) is not dict:
            raise InvalidParameter("payload was expected dict, got {}".format(type(payload).__name__))

        payload = self.validate(payload)

        # Automagically appends the api key if it was not done before
        if "k" not in payload.keys():
            payload["k"] = self.key

        # Sends an async request and parses json with ujson
        session = self._handle_session()

        async with session.get(self._build_url(endpoint, **payload)) as resp:
            if 200 < resp.status <= 300:
                # Anything other than 200 is not good
                raise ConnectorException("Response code is {} {}".format(resp.status, resp.reason))

            # Converts to json format
            return await resp.json()
