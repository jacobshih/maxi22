#! /usr/bin/env python3
################################################################################
"""
uds.py: unix domain socket.
"""
# noinspection PyUnresolvedReferences
import parentpath
import json

from tools.aap import AnotherArgumentParser
from tools.uds import UDSServer, UDSClient


class IPCDaemon(UDSServer):
    log_client = None

    def __init__(self, sockfile, echo=False):
        UDSServer.__init__(self, sockfile)
        self.echo = echo

    def onreceive(self, data):
        if self.echo:
            if self.connection:
                _ = self.connection.send(data)
            pass
        pass

    def send_ipc_response(self, data):
        return


class IPCClient(UDSClient):
    async = False

    def __init__(self, sockfile, async=False):
        UDSClient.__init__(self, sockfile)
        self.async = async

    def onsend(self, data):
        resp = ""
        if not self.async:
            resp = self._socket.recv(self.RECEIVED_SIZE)

        return resp


class UDSService:
    args = None

    def __init__(self):
        pass

    def ipcdaemon(self):
        args = self.args
        sockfile = args.sockfile
        echo = args.echo
        if sockfile:
            daemon = IPCDaemon(sockfile, echo)
            daemon.start()
            daemon.run()
            daemon.stop()
        return

    def ipcclient(self):
        args = self.args
        sockfile = args.sockfile
        if sockfile:
            data = args.data
            async = args.async
            client = IPCClient(sockfile, async)
            client.start()
            resp = client.send(data)
            respstr = resp.decode()
            jso = json.loads(respstr)
            print(json.dumps(jso, indent=2))
            client.stop()
        return

    def run(self, args, parser=None):
        self.args = args
        action = args.action if "action" in args else None
        if action is not None:
            exec("self.%s()" % action)
        else:
            print(parser.parse_args(["-h"]))
        return


def init_args_parser():
    parser = AnotherArgumentParser(description="======  uds service  ======")
    subparsers = parser.add_subparsers(title="action", help="the actions")

    # create the parser for the "ipc" command
    parser_ipc = subparsers.add_parser("ipc", help="inter-process communication.")
    subparsers_ipc = parser_ipc.add_subparsers(title="ipc", help="the actions of the ipc")

    # create the parser for the "ipc daemon" command
    parser_ipc_daemon = subparsers_ipc.add_parser("daemon", help="run a ipc daemon.")
    parser_ipc_daemon.add_argument("-s", "--sockfile", required=True, help="domain socket path.")
    parser_ipc_daemon.add_argument("-e", "--echo", action="store_true", default=False,
                                   help="reply the received data automatically.")
    parser_ipc_daemon.set_defaults(action="ipcdaemon")

    # create the parser for the "ipc client" command
    parser_ipc_client = subparsers_ipc.add_parser("client", help="run a ipc client.")
    parser_ipc_client.add_argument("-s", "--sockfile", required=True, help="domain socket path.")
    parser_ipc_client.add_argument("-d", "--data", required=True, help="ipc data.")
    parser_ipc_client.add_argument("-a", "--async", action="store_true", default=False,
                                   help="send data asynchronously without waiting for response.")
    parser_ipc_client.set_defaults(action="ipcclient")

    return parser


def main():
    global args_parser
    args_parser = init_args_parser()
    args = args_parser.parse_args()

    udss = UDSService()
    udss.run(args, parser=args_parser)


################################################################################

if __name__ == "__main__":
    main()
    pass
