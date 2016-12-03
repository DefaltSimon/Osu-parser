# coding=utf-8

__author__ = "DefaltSimon"


class OsuError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class ConnectorException(OsuError):
    def __init__(self, *args, **kwargs):
        pass


class InvalidParameter(OsuError):
    def __init__(self, *args, **kwargs):
        pass
