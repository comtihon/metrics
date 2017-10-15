"""Metric integration test tool

Usage:
  survey_tester [-t TESTS]
  survey_tester -v | --version
  survey_tester -h | --help

Options:
  -h --help                          show this help message and exit
  -t TESTS --test=TESTS              test names to be run, comma separated (from tester.test package) [default: all].
  -v --version                       print version and exit
"""

import sys

from colorama import init, Fore
from docopt import docopt, DocoptExit

import tester
from tester.system.tests_runner import TestsRunner


def get_args(args, vsn):
    try:
        return docopt(__doc__, argv=args, version=vsn)
    except DocoptExit as usage:
        print(usage)
        sys.exit(1)


def main(args=None):
    init(autoreset=True)
    arguments = get_args(args, tester.vsn)
    print(Fore.GREEN + 'Metric tester ' + tester.vsn)
    tests_runner = TestsRunner(arguments)
    if tests_runner.run():
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
