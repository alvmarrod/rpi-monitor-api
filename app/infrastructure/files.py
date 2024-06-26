"""Handles all the SO file data extraction, taking into consideration any
relative information required, like number of cores"""

import re
import logging

from typing import Optional

##############################################################################
#                                 Constants                                  #
##############################################################################

CPU_INFO_FILEPATH: str = '/proc/cpuinfo'
CPU_PROC_FILEPATH: str = '/proc/loadavg'

MEM_INFO_FILEPATH: str = '/proc/meminfo'

NET_INFO_FILEPATH: str = '/proc/net/dev'
NET_INFO_HEADER_SIZE: int = 2

##############################################################################
#                                 Aux Functions                              #
##############################################################################

def _process_mem_string(line: str) -> int:
    """Process the given line expecting the format from /proc/meminfo file lines,
    and returns the given Ki as int
    e.g.
    MemTotal:        7795016 kB
    """
    kibit: int = -1
    memregex: str = r'Mem[\w]+:[\s]*([\d]+) kB$'

    result: Optional[re.Match] = re.match(memregex, line)

    if result is not None:
        try:
            kibit = int(result.groups()[0])
        except Exception:
            logging.error("Error trying to convert mem info into integer: %s", result[0])

    return kibit

def _proc_net_string(line: str) -> tuple[str, dict[str, int]]:
    """Process the given line expecting the format from /proc/net/dev file lines,
    returning a tuple with the interface name and the data for that interface.
    
    Returns a tuple with empty string and empty dict if any error is found"""
    iface: str = ""
    iface_data: dict[str, int] = {}

    try:

        # Collapse spaces
        line = ' '.join(line.split())

        parts: list[str] = line.split(" ")

        iface = parts[0].replace(":", "")
        iface_data = {
            "rec_pack"  : int([parts[2]]),
            "rec_bytes" : int([parts[1]]),
            "rec_err"   : int([parts[3]]),
            "rec_drop"  : int([parts[4]]),

            "snd_pack"  : int([parts[10]]),
            "snd_bytes" : int([parts[9]]),
            "snd_err"   : int([parts[11]]),
            "snd_drop"  : int([parts[12]])
        }


    except Exception as err:
        logging.error("Error trying to process net info: %s", err)

    return iface, iface_data

##############################################################################
#                              Public Functions                              #
##############################################################################

async def get_cpu_cores() -> int:
    """Check number of cores available in the CPU.
    
    Defaults to -1 if any error found"""
    cores: int = 0

    try:

        with open(CPU_INFO_FILEPATH, 'r', encoding='utf8') as cpu_reader:
            for line in cpu_reader:
                if 'processor' in line:
                    cores += 1

    except FileNotFoundError:
        logging.warning("Can't find expected CPU INFO file at: %s", CPU_INFO_FILEPATH)
    except Exception as err:
        logging.warning("Unexpected error:\n%s", err)
    finally:
        cores = cores if cores != 0 else -1

    logging.debug("Detected CPU Cores: %i", cores)
    return cores

async def get_cpu_load_avg() -> dict[str, str]:
    """Read the system CPU Load information and return in dictionary format,
    parsed to float.
    
    Will return -1 for each load average if any error is found"""
    load_avg: dict[str, str] = {}

    try:

        with open(CPU_PROC_FILEPATH, 'r', encoding='utf8') as load_reader:
            loads: list[str] = load_reader.readline().split(" ")[0:3]

            load_avg["1m"] = loads[0]
            load_avg["5m"] = loads[1]
            load_avg["15m"] = loads[2]

    except Exception as err:
        logging.warning("Unexpected error:\n%s", err)

    return load_avg

async def get_mem_info() -> dict[str, int]:
    """Read the system Memory information and return in dictionary format,
    in kbi parsed to integer.
    
    Will return -1 for each memory amount if any error is found"""
    mem_info: dict[str, int] = {}

    try:

        with open(MEM_INFO_FILEPATH, 'r', encoding='utf8') as mem_reader:
            mem_info['mem_total'] = _process_mem_string(mem_reader.readline())
            mem_info['mem_free'] = _process_mem_string(mem_reader.readline())
            mem_info['mem_ava']  = _process_mem_string(mem_reader.readline())

    except Exception as err:
        logging.warning("Unexpected error:\n%s", err)

    return mem_info

async def get_net_info() -> dict[str, dict[str, int]]:
    """Read the system network interfaces information and return in dictionary format.
    
    Will return an empty dict if any error is found."""
    net_info: dict[str, dict[str, int]] = {}

    try:
        header: int = 0
        with open(NET_INFO_FILEPATH, 'r', encoding='utf8') as net_reader:
            iface_name: str
            iface_data: dict[str, int]

            for line in net_reader:
                if header < NET_INFO_HEADER_SIZE:
                    header += 1
                    continue

                iface_name, iface_data = _proc_net_string(line)
                net_info[iface_name] = iface_data

    except Exception as err:
        logging.warning("Unexpected error:\n%s", err)

    return net_info
