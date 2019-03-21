from __future__ import print_function
from subprocess import Popen, PIPE
import os
import sys
import shlex
import logging
import yaml
import click
from plumbum import local
from plumbum import TEE
from plumbum import BG
from plumbum.commands import ProcessExecutionError
import build_utilities

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)


def check_anaconda_login():
    try:
        login_info = build_utilities.call_binary("anaconda", ["whoami"], silent=True, stderr_output=True)
    except ProcessExecutionError:
        print("You are not logged into the Anaconda CLI.  Please login before running the script")
        sys.exit(1)

    login_list = login_info.split("\n")
    if 'Anonymous User' in login_list:
        print("You are not logged into the Anaconda CLI.  Please login before running the script")
        sys.exit(1)

    login_dict = {}
    for val in login_list:
        pair = val.split(": ")
        if pair[0]:
            key = pair[0].strip()
            login_dict[key.lstrip("+")] = pair[1]

    print("Logged into the Anaconda CLI as {}".format(login_dict["Username"]))


@click.command()
@click.option('--origin', default="conda-forge", help='Name of the conda channel to copy packages from')
@click.option('--destination', default="esgf", help='Name of the conda channel to copy packages to')
@click.option('--env', default=None, help='Name of the conda environment for which to upload the packages it contains')
def main(env, origin, destination):
    if env is None:
        env_file_name = input("Enter the name of the conda environment file to parse:")
    else:
        env_file_name = env

    with open(os.path.join(os.path.dirname(__file__), env_file_name), 'r') as config_file:
        config = yaml.load(config_file)

    dependencies = config["dependencies"][:-1]
    print("conda dependencies:")
    print("\n".join(dependencies))

    check_anaconda_login()

    failed = []
    success = []

    print("Uploading packages for environment: {}".format(env_file_name))
    for dependency in dependencies:
        try:
            name, version = dependency.split("=")
        except ValueError:
            name = dependency
            version = None
        print("name:", name)
        print("version:", version)
        if name == "#":
            continue
        if version is None:
            resource_location = "{}/{}".format(origin, name)
        else:
            resource_location = "{}/{}/{}".format(origin, name, version)
        print("Copying {} version {}".format(name, version))
        try:
            output = build_utilities.call_binary("anaconda", ["copy", resource_location, "--to-owner", destination])
            success.append((name, version))
        except ProcessExecutionError:
            failed.append((name, version))

    print("Successfully copied the following packages to the esgf conda channel")
    for package in success:
        print(package)

    print("The following packages failed to be copied.")
    for package in failed:
        print(package)

if __name__ == '__main__':
    main()
