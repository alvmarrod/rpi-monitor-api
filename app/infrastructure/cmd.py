"""Handles the execution of external commands to retrieve information,
allowing to execute only a subset of commands for security"""

import os
import re
import logging

from typing import Optional, Union

##############################################################################
#                                 Constants                                  #
##############################################################################

ALLOWED_OS_COMMANDS: list[str] = [
    'ls',
    'df',
    'iwconfig'
]

# Forbidden syntax for security reasons
FORBIDDEN_SYNTAX: list[str] = [
    ';', '&&', '||', '`', '$', '(', ')', '{', '}', '<', '>'
]

##############################################################################
#                                 Aux Functions                              #
##############################################################################

def _is_command_allowed(command: str) -> bool:
    """Checks if a command is allowed to be executed"""
    not_allowed: bool = True

    not_allowed = any([character in command for character in FORBIDDEN_SYNTAX])

    if not not_allowed:
        not_allowed = command.split()[0] not in ALLOWED_OS_COMMANDS

    return not not_allowed

def exec_cmd(command: str) -> Optional[str]:
    """Execute the given command and return the output"""
    result: Optional[str] = None
    if not _is_command_allowed(command):
        logging.error("Command not allowed: %s", command)

    try:
        result = os.popen(command).read()
    except Exception as err:
        logging.error("Error executing command: %s", str(err))

    return result

def parse_df_output(output: str) -> dict[str, dict[str, Union[int, str]]]:
    """Parse the output from the df command"""
    disk_data: dict[str, dict[str, Union[int, str]]] = {}

    lines: list[str] = output.split('\n')
    header: bool = True

    for line in lines:
        if header:
            header = False
            continue

        if line:
            parts: list[str] = line.split()
            disk_data[parts[0]] = {
                "total": int(parts[1]),
                "used": int(parts[2]),
                "free": int(parts[3]),
                "mount": parts[5]
            }

    return disk_data

def parse_net_output(output: str) -> dict[str, str]:
    """Parse the output from the iwconfig command"""
    net_data: dict[str, int] = {}

    supported_keys: dict[str, str] = {
        "bit_rate": r"Bit Rate=([\d|.]+ [M|G]b/s)",
    }

    lines: list[str] = output.split('\n')

    for line in lines:
        for key, regex in supported_keys.items():
            reg_result: Optional[re.Match] = re.search(regex, line)
            if reg_result is not None:
                net_data[key] = reg_result.groups()[0]

    return net_data

##############################################################################
#                              Public Functions                              #
##############################################################################

def get_disk_usage() -> dict[str, dict[str, Union[int, str]]]:
    """Retrieve file system disk space usage using df command"""
    disk_data: dict[str, dict[str, Union[int, str]]] = {}

    cmd: str = 'df'
    raw_disk_data: Optional[str] = exec_cmd(cmd)

    if raw_disk_data is not None:
        disk_data = parse_df_output(raw_disk_data)

    return disk_data

def get_net_info(iface_name: str) -> dict[str, str]:
    """Retrieve network interfaces information using iwconfig command"""
    net_data: dict[str, int] = {}

    cmd: str = 'iwconfig ' + iface_name
    raw_net_data: Optional[str] = exec_cmd(cmd)

    if raw_net_data is not None:
        net_data = parse_net_output(raw_net_data)

    return net_data
