#! /usr/bin/env python3
################################################################################
"""
aap.py: another argument parser

  * AnotherArgumentParser - another argument parser.
"""

import argparse
import sys

__all__ = []


def export(obj):
    __all__.append(obj.__name__)
    return obj


@export
class AnotherArgumentParser(argparse.ArgumentParser):
    """
    AnotherArgumentParser is subclassed from argparse.ArgumentParser and
    overrides the method error() to print a customized message while the
    command line arguments are parsed error. it prints the error and show
    the command line help if error occurs.
    """

    def error(self, message):
        sys.stderr.write("\n[ERROR] %s\n\n" % message)
        self.print_help()
        sys.exit(2)

