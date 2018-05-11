#! /usr/bin/env python3
################################################################################
"""
uds.py: unix domain socket.

  * UDS - base class of unix domain socket.
  * UDSServer - generic UDS server.
  * UDSClient - generic UDS client.
"""

import os
import sys
import abc
import signal
import socket
import uuid


class UDS(object):
    _sockfile = None
    RECEIVED_SIZE = 1024

    def __init__(self, sockfile):
        self._sockfile = sockfile

    @property
    def sockfile(self):
        return self._sockfile

    @sockfile.setter
    def sockfile(self, sockfile):
        self._sockfile = sockfile

    # noinspection PyProtectedMember
    def log(self, msg):
        class_name = self.__class__.__name__
        func_name = sys._getframe().f_code.co_name
        print("*** {}.{}() *** {}".format(class_name, func_name, msg))


class UDSServer(UDS, metaclass=abc.ABCMeta):
    _socket = None
    _connection = None
    _peeraddress = None
    _listening = True

    def __init__(self, sockfile):
        UDS.__init__(self, sockfile)

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, connection):
        self._connection = connection

    @property
    def listening(self):
        return self._listening

    @listening.setter
    def listening(self, listening):
        self._listening = listening

    def start(self):
        if os.path.exists(self.sockfile):
            os.remove(self.sockfile)
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._socket.bind(self.sockfile)
        self._socket.settimeout(1)
        self._socket.listen(0)

    def stop(self):
        if self._socket:
            try:
                self._socket.close()
                os.remove(self.sockfile)
                self._socket = self._connection = self._peeraddress = None
            finally:
                pass

    def run(self):
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        try:
            while self.listening:
                try:
                    connection, _ = self._socket.accept()
                except socket.timeout:
                    pass
                except Exception:
                    raise
                else:
                    self.connection = connection
                    while self.listening:
                        data = connection.recv(self.RECEIVED_SIZE)
                        if not data:
                            break
                        else:
                            self.onreceive(data)

        except KeyboardInterrupt as _:
            pass
        except OSError as _:
            pass
        finally:
            self.stop()

    @abc.abstractmethod
    def onreceive(self, data):
        pass

    # noinspection PyUnusedLocal
    def exit_gracefully(self, signum, frame):
        self.listening = False


class UDSClient(UDS, metaclass=abc.ABCMeta):
    _socket = None

    def __init__(self, sockfile):
        UDS.__init__(self, sockfile)

    def start(self):
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self._socket.connect(self.sockfile)
        except socket.error as e:
            self.log(str(e))
            self.stop()

    def stop(self):
        if self._socket:
            self._socket.close()
            self._socket = None

    def send(self, data):
        resp = ""
        if self._socket:
            try:
                self._socket.send(data.encode())
                resp = self.onsend(data)
            except IOError as e:
                print(e)
                print(uuid.ctypes.create_string_buffer(data).value.decode())
        return resp

    @abc.abstractmethod
    def onsend(self, data):
        return ""

