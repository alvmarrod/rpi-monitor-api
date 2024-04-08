"""Defines data model and domain entities for CPU domain"""

import json
import logging
import dataclasses as dc

import app.infrastructure.files as infra_files

##############################################################################
#                                Data Model                                  #
##############################################################################

@dc.dataclass
class CPULoadAvgs:
    """Models CPU Load Averages"""
    m1:     float = -1
    m5:     float = -1
    m15:    float = -1

    def __str__(self) -> str:
        """Overwrite class representation"""
        return json.dumps(dc.asdict(self))

##############################################################################
#                               Aux Functions                                #
##############################################################################

def _transform_cpu_load_percentage(load: str, cores: int) -> float:
    """Returns the CPU load as percentage based on the number of cores
    
    Defaults to -1 if any error found"""
    float_load: float = float(load) * 100/cores

    try:
        float_load: float = float(load) * 100/cores

    except Exception as err:
        logging.warning("Couldn't format properly load average:\n%s", str(err))

    return float_load

##############################################################################
#                              Public Functions                              #
##############################################################################

async def read_cpu_info() -> CPULoadAvgs:
    """Read the system CPU Load information and return in dictionary format,
    parsed to float.
    
    Will return -1 for each load average if any error is found"""
    load_avgs: CPULoadAvgs = CPULoadAvgs()

    try:
        cpu_cores: int = await infra_files.get_cpu_cores()
        cpu_avg_loads: dict[str, str] = await infra_files.get_cpu_load_avg()

        load_avgs.m1 = _transform_cpu_load_percentage(cpu_avg_loads["1m"], cpu_cores)
        load_avgs.m5 = _transform_cpu_load_percentage(cpu_avg_loads["5m"], cpu_cores)
        load_avgs.m15 = _transform_cpu_load_percentage(cpu_avg_loads["15m"], cpu_cores)

    except Exception as err:
        logging.warning("Unexpected error reading CPU info:\n%s", str(err))

    return load_avgs
