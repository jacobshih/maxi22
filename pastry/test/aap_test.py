#! /usr/bin/env python3
################################################################################
"""
aap_test.py: test aap (another argument parser) module
"""
# noinspection PyUnresolvedReferences
import parentpath
from tools.aap import AnotherArgumentParser


class AAP:
    args = None

    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def first_help(self):
        print(args_parser.parse_args(["first", "-h"]))
        return

    # noinspection PyMethodMayBeStatic
    def second_help(self):
        print(args_parser.parse_args(["second", "-h"]))
        return

    # noinspection PyMethodMayBeStatic
    def first_one_action(self):
        print("first one action")
        return

    # noinspection PyMethodMayBeStatic
    def first_two_action(self):
        print("first two action")
        return

    # noinspection PyMethodMayBeStatic
    def second_action(self):
        print("second action")
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
    parser = AnotherArgumentParser(description="======  aap test  ======")
    subparsers = parser.add_subparsers(title="action", help="the actions")

    # create the parser for the "first" command
    parser_first = subparsers.add_parser("first", help="first command.")
    subparsers_first = parser_first.add_subparsers(title="first", help="the actions of the first")
    parser_first.set_defaults(action="first_help")

    # create the parser for the "first one" command
    parser_first_one = subparsers_first.add_parser("one", help="first one.")
    parser_first_one.add_argument("-a", "--apple", required=True, help="what is apple.")
    parser_first_one.add_argument("-b", "--banana", action="store_true", default=False, help="what is banana.")
    parser_first_one.set_defaults(action="first_one_action")

    # create the parser for the "first two" command
    parser_first_two = subparsers_first.add_parser("two", help="first two.")
    parser_first_two.add_argument("-c", "--cream", required=True, help="what is cream.")
    parser_first_two.add_argument("-d", "--dumpling", action="store_true", default=False, help="what is dumpling.")
    parser_first_two.set_defaults(action="first_two_action")

    # create the parser for the "second" command
    parser_second = subparsers.add_parser("second", help="second command.")
    # subparsers_second = parser_second.add_subparsers(title="second", help="the actions of the second")
    parser_second.add_argument("-e", "--egg", required=True, help="what is egg.")
    parser_second.add_argument("-f", "--fruit", action="store_true", default=False, help="what is fruit.")
    parser_second.set_defaults(action="second_action")

    return parser


def main():
    global args_parser
    args_parser = init_args_parser()
    args = args_parser.parse_args()

    aap = AAP()
    aap.run(args, parser=args_parser)


################################################################################

if __name__ == "__main__":
    main()
    pass
