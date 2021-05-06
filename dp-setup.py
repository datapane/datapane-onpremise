#!/usr/bin/env python3
"""
Datapane Server script

"""

from ast import literal_eval
import json
import time
import datetime

datetime.datetime.now().ctime()
from contextlib import suppress
from distutils.util import strtobool
import argparse
import sys
import logging
import os
import secrets
from enum import Enum
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, TextIO, Tuple

log = logging.getLogger("dp-setup")


# commands
# TODO - start/stop local trial
def check(args):
    """Check all (docker) dependencies are installed"""
    docker_exe = shutil.which("docker")
    if docker_exe:
        log.debug(f"Found docker at {docker_exe}")
        subprocess.run([docker_exe, "--version"], check=True)
        subprocess.run([docker_exe, "info"], check=True, capture_output=True)
    else:
        sys.exit("docker not found, please install")

    docker_compose_exe = shutil.which("docker-compose")
    if docker_compose_exe:
        log.debug(f"Found docker-compose at {docker_compose_exe}")
        subprocess.run(["docker-compose", "--version"], check=True)
    else:
        sys.exit("docker-compose not found, please install")

    print("Dependencies all provided, please run `configure` to generate your config file")


def configure(args):
    """
    Configure the on-prem instance (for docker-compose only at present),
    generates a docker-compose.yml and datapane.env suitable for running

    # TODO - future questions
    # - cloud provider? not right now, S3 only - see Provider enum in django config
    # - optional redis
    # - domain - allowed hosts config
    # - https
    """

    print("👋 Hi! I'm here to help you set up a self-hosted Datapane Server.\n")

    print("Datapane can run with in dev mode with all dependencies, or in prod mode using managed cloud services, such as AWS RDS. " +
          "We recommend dev mode for trying out, and prod mode for longer term deployments.")

    while True:
        with suppress(ValueError):
            prod_mode = strtobool(input("Run in prod mode (Yes/No)? "))
            break

    template = Path("docker/datapane.env").read_text()
    if prod_mode:
        print("Building prod docker-compose configuration")
        shutil.copyfile("docker/docker-compose.prod.yml", "docker-compose.yml")
    else:
        print("Building dev docker-compose configuration")
        shutil.copyfile("docker/docker-compose.dev.yml", "docker-compose.yml")

    output = template.format(
        configuration="OrgOnPrem",
        django_secret_key=secrets.token_urlsafe(50),
    )

    out_env = Path("datapane.env")
    if out_env.exists():
        backup_env = f"datapane.env.{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        log.debug(f"Found old env, saving as {backup_env}")
        shutil.copyfile(out_env, backup_env)
    out_env.write_text(output)

    print("\n👍 Thanks! Now edit the datapane.env as needed, add your license key, and run `docker-compose up` to launch Datapane! 🍀")


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
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    log.debug(args)

    if args.command:
        args.command(args)
    else:
        sys.exit("No command entered, use --help")


if __name__ == "__main__":
    # check deps
    assert sys.version_info.minor >= 6, "Require Python 3.6 or above"
    main()
