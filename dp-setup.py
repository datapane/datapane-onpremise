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


def update(args):
    print("update")
    print(args)
    # sudo docker-compose build --pull
    # sudo docker-compose pull && sudo docker-compose up -d
    # sudo docker image prune -a -f


def start(args):
    print("start")
    print(args)


def stop(args):
    print("stop")
    print(args)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Configure the arg parser"""
    parser = argparse.ArgumentParser(description="Setup and configure an on-premise Datapane Server",
                                     epilog="For more info see https://github.com/datapane/datapane-onpremise/ and https://docs.datapane.com/deployment/")
    # main args
    parser.add_argument("--debug", action="store_true", default=False, help="Enable debug output")
    subparsers = parser.add_subparsers(help='Available commands', dest="command")

    # subcommands
    parser_check = subparsers.add_parser("check",  help="Check all dependencies are installed")
    parser_check.set_defaults(command=check)

    parser_configure = subparsers.add_parser("configure",  help="Configure the datapane environment file")
    parser_configure.add_argument("--env", help="The cloud environment")
    parser_configure.set_defaults(command=configure)

    parser_update = subparsers.add_parser("update",  help="Update Datapane Server to latest version")
    parser_update.set_defaults(command=update)

    parser_start = subparsers.add_parser("start",  help="Start Datapane Server (via docker-compose)")
    parser_start.set_defaults(command=start)

    parser_stop = subparsers.add_parser("stop",  help="Stop Datapane Server (via docker-compose)")
    parser_stop.set_defaults(command=stop)

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
