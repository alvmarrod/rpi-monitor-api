"""Defines data model and domain entities for Memory domain"""

import json
import logging
import dataclasses as dc

import app.infrastructure.files as infra_files

##############################################################################
#                                Data Model                                  #
##############################################################################

@dc.dataclass
class RAMRawInfo:
    """Models Raw RAM Info. Storage unit is bytes"""
    mem_total    : int = -1
    mem_free     : int = -1
    mem_ava      : int = -1
    mem_used     : int = -1

    def __str__(self) -> str:
        """Overwrite class representation"""
        return json.dumps(self.as_dict())

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in ['mem_total', 'mem_ava']:
            self.mem_used = self.mem_total - self.mem_ava

    def as_dict(self, unit: str = "B") -> dict:
        """Return the class as a dictionary. The unit can be changed"""

        unit_order: int = 1
        available_units: list[str] = ["B", "kB", "MB", "GB"]

        if unit in available_units:
            unit_order += available_units.index(unit)

        total = self.mem_total / (1024 ** unit_order)
        free = self.mem_free / (1024 ** unit_order)
        ava = self.mem_ava / (1024 ** unit_order)
        used = self.mem_used / (1024 ** unit_order)
        return {
            "total": total,
            "free": free,
            "ava": ava,
            "used": used
        }

##############################################################################
#                               Aux Functions                                #
##############################################################################

##############################################################################
#                              Public Functions                              #
##############################################################################

async def read_ram_info() -> RAMRawInfo:
    """Read the system Memory information and return in dictionary format,
    in kbi parsed to integer.
    
    Will return -1 for each memory amount if any error is found"""
    ram: RAMRawInfo = RAMRawInfo()

    try:
        ram_raw: dict[str, int] = await infra_files.get_mem_info()

        ram.mem_total = ram_raw['mem_total'] * 1024
        ram.mem_free = ram_raw['mem_free'] * 1024
        ram.mem_ava = ram_raw['mem_ava'] * 1024

    except Exception as err:
        logging.warning("Unexpected error:\n%s", err)

    return ram
