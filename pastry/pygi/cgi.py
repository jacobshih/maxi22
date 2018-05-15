#! /usr/bin/env python3
################################################################################
"""
cgi.py: abstract class of pygi applications.
"""
import abc
import os
from tools.uds import UDSClient


__all__ = []


def export(obj):
    __all__.append(obj.__name__)
    return obj


@export
class CGI(metaclass=abc.ABCMeta):
    SOCKET_PATH = "/tmp/grocer.sock"
    HTTP_HEADER = {
                "Content-type": "text/json",
                "Cache-Control": "no-store"
            }
    _env = None
    _path = None
    _value = None
    _data = None
    _ipc_client = None
    _socket_path = None
    _http_header = {}

    def __init__(self, socket_path=None, http_header=None):
        # retrieve environment variables
        self._env = os.environ

        # set default http header
        if http_header is None:
            self.http_header = CGI.HTTP_HEADER
        else:
            self.http_header = http_header

        # initialize ipc client
        if socket_path is None:
            self._socket_path = CGI.SOCKET_PATH
        else:
            self.socket_path = socket_path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def socket_path(self):
        return self._socket_path

    @socket_path.setter
    def socket_path(self, socket_path):
        self._socket_path = socket_path

    @property
    def http_header(self):
        return self._http_header

    @http_header.setter
    def http_header(self, http_header):
        self._http_header = http_header

    def start(self):
        self._ipc_client = IPCClient(self._socket_path)
        self._ipc_client.start()
        pass

    def get(self, path):
        self.path = path
        self.value = self._ipc_client.send(path)
        return self.value

    def set(self, path, value):
        self.path = path
        self.value = value
        pass

    def send_response(self, data):
        self.data = data
        print(self.data)
    pass

    def send_http_header(self, http_header=None):
        if http_header is None:
            http_header = self.http_header
        s = ""
        for k in http_header.keys():
            s += k + ": " + http_header[k] + "\r\n"
        print(s)
    pass


class IPCClient(UDSClient):
    async = False

    def __init__(self, sockfile, async=False):
        UDSClient.__init__(self, sockfile)
        self.async = async

    def onsend(self, data):
        resp = ""
        if not self.async:
            resp = self._socket.recv(self.RECEIVED_SIZE)
            # process response data here

        return resp


