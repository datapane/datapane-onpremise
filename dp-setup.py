#!/usr/bin/env python3
"""
Datapane Server script

"""

import argparse
import sys
import logging
import os
import secrets
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, TextIO, Tuple

log = logging.getLogger("dp-setup")


# commands
# start/stop local trial
# check deps (docker & docker compose)
# upgrade
# setup/configure

def check(args):
    print("check")
    log.debug("debug")
    log.info("info")
    print(args)


def configure(args):
    print("configure")
    print(args)




def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    # TODO - min version param
    parser = argparse.ArgumentParser(description="Setup and configure an on-premise Datapane Server",
                                     epilog="For more info see https://github.com/datapane/datapane-onpremise/ and https://docs.datapane.com/deployment/")
    parser.add_argument("--debug", action="store_true", default=False, help="Enable debug output")

    subparsers = parser.add_subparsers(help='Available commands', dest="command")
    parser_check = subparsers.add_parser("check",  help="Check all dependencies are installed")
    parser_check.set_defaults(command=check)

    parser_configure = subparsers.add_parser("configure",  help="Configure the datapane environment file")
    parser_configure.add_argument("--env", help="The cloud environment")
    parser_configure.set_defaults(command=configure)

    return parser.parse_args(argv)


def main():
    args = parse_args()
    print(args)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    if args.command:
        args.command(args)


if __name__ == "__main__":
    # check deps
    assert sys.version_info.minor >= 6, "Require Python 3.6 or above"
    main()
