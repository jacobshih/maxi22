#! /usr/bin/env python3
################################################################################
"""
cgi_test.py: test pygi module
"""
# noinspection PyUnresolvedReferences
import parentpath
from pygi.cgi import CGI


class CGITest(CGI):
    def __init__(self):
        CGI.__init__(self)
        pass


def main():
    cgi_test = CGITest()
    cgi_test.start()
    value = cgi_test.get("/config/group00/name00")
    cgi_test.set("/config/group00/name00", value)
    cgi_test.send_http_header()
    cgi_test.send_response(value.decode())
    pass


################################################################################

if __name__ == "__main__":
    main()
    pass
