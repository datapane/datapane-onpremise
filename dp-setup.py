#!/usr/bin/env python3
"""
Datapane Server script

"""

import argparse
import sys
import logging
import os
import secrets
from enum import Enum
from shutil import which
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, TextIO, Tuple

log = logging.getLogger("dp-setup")


# commands
# TODO - start/stop local trial
def check(args):
    """Check all (docker) dependencies are installed"""
    docker_exe = which("docker")
    if docker_exe:
        log.debug(f"Found docker at {docker_exe}")
        subprocess.run([docker_exe, "--version"], check=True)
        subprocess.run([docker_exe, "info"], check=True, capture_output=True)
    else:
        sys.exit("docker not found, please install")

    docker_compose_exe = which("docker-compose")
    if docker_compose_exe:
        log.debug(f"Found docker-compose at {docker_compose_exe}")
        subprocess.run(["docker-compose", "--version"], check=True)
    else:
        sys.exit("docker-compose not found, please install")

    print("Dependencies all provided, please run `configure` to generate your config file")


def configure(args):
    print("configure")


def update(args):
    """Update the docker containers"""
    subprocess.run(["sudo", "docker-compose", "build", "--pull"], check=True)
    subprocess.run(["sudo docker-compose pull && sudo docker-compose up -d"], shell=True, check=True)
    subprocess.run(["sudo", "docker", "image", "prune", "-a", "-f"], check=True)


def start(args):
    subprocess.run(["sudo docker-compose up -d"], shell=True, check=True)


def stop(args):
    subprocess.run(["sudo docker-compose down"], shell=True, check=True)


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
    else:
        sys.exit("No command entered, use --help")


if __name__ == "__main__":
    # check deps
    assert sys.version_info.minor >= 6, "Require Python 3.6 or above"
    main()
