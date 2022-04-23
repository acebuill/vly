"""
Vly


Usage:
    vly (install|uninstall) <groupname>
    vly (disable|enable) <mirror_name>
    vly set_parallel <number_of_parallel_downloads>

Options:
    --rup  Remove unnecessary packages
"""

from docopt import docopt
from log import log, log_err
import sys
import yaml
import pacman
import pacmanconfig
import vlyconf


def get_action(arguments: dict) -> str:
    for key in arguments:
        if isinstance(arguments[key], bool) and arguments[key]:
            return key


def get_action_value(action: str, arguments: dict) -> str:
    return {
        "install": "<groupname>",
        "uninstall": "<groupname>",
        "disable": "<mirror_name>",
        "enable": "<mirror_name>",
        "set_parallel": "<number_of_parallel_downloads>",
    }[action]


def check_values(action_value: str, arguments: dict) -> bool:
    log("checking values")
    if action_value == "<number_of_parallel_downloads>":
        try:
            int(arguments[action_value])
            return True
        except:
            log_err(action_value + " must be an integer")
            sys.exit(1)
    return {
        "<groupname>": str,
        "<mirror_name>": str,
        "<number_of_parallel_downloads>": int,
    }[action_value] == type(arguments[action_value])


def handle_required_repository(group: dict) -> bool:
    refresh_required = False
    if not pacmanconfig.mirror_is_enabled(group["required_repository"]):
        log(f'enabling required {group["required_repository"]}')
        pacmanconfig.enable_repository(group["required_repository"])
        refresh_required = True
    return refresh_required


def execute_group_action(arguments: dict):
    try:
        group = vlyconf.retrieve_group(arguments["<groupname>"])
    except:
        log_err(arguments["<groupname>"] + "is not defined in the config file")
        sys.exit(1)
    if arguments["install"]:
        refresh_required = False
        if "required_repository" in group:
            refresh_required = handle_required_repository(group)
        return pacman.install_packages(
            group["packages"],
            refresh_repositories=group["refresh"],
        )
    elif arguments["uninstall"]:
        return pacman.uninstall_packages(group["packages"], True)


def execute_repository_action(arguments):
    if arguments["enable"]:
        pacmanconfig.enable_repository(
            arguments["<mirror_name>"]
        )
        return True
    pacmanconfig.disable_repository(
        arguments["<mirror_name>"]
    )


def execute_action(arguments: dict) -> bool:
    if arguments["<groupname>"] != None:
        execute_group_action(arguments)
    if arguments["<mirror_name>"] != None:
        execute_repository_action(arguments)
    if arguments["<number_of_parallel_downloads>"] != None:
        pacmanconfig.set_number_of_parallel_downloads(arguments["<number_of_parallel_downloads>"])


def main():
    arguments = docopt(__doc__)
    execute_action(arguments)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nexiting ...")
        sys.exit(1)
