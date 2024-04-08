"""Defines data model and domain entities for Network domain"""

import json
import logging
import dataclasses as dc

import app.infrastructure.cmd as infra_cmd
import app.infrastructure.files as infra_files

##############################################################################
#                                Data Model                                  #
##############################################################################

@dc.dataclass
class IfaceInfo:
    """Models Raw Net Info. Storage unit is bytes"""
    rx_pack      : int = -1
    rx_bytes     : int = -1
    rx_err       : int = -1
    rx_drop      : int = -1
    tx_pack      : int = -1
    tx_bytes     : int = -1
    tx_err       : int = -1
    tx_drop      : int = -1
    bit_rate      : str = "- Mb/s"

    def __str__(self) -> str:
        """Overwrite class representation"""
        return json.dumps(self.as_dict())

    def as_dict(self, unit: str = "B") -> dict:
        """Return the class as a dictionary. The unit can be changed"""

        unit_order: int = 1
        available_units: list[str] = ["B", "kB", "MB", "GB"]

        if unit in available_units:
            unit_order += available_units.index(unit)

        rx_pack    : int = self.rx_pack
        rx_bytes   : int = self.rx_bytes / (1024 ** unit_order)
        rx_drop    : int = self.rx_drop
        rx_err     : int = self.rx_err

        tx_pack    : int = self.tx_pack
        tx_bytes   : int = self.tx_bytes / (1024 ** unit_order)
        tx_drop    : int = self.tx_drop
        tx_err     : int = self.tx_err

        return {
            "rx_pack": rx_pack,
            "rx_bytes": rx_bytes,
            "rx_err": rx_err,
            "rx_drop": rx_drop,
            "tx_pack": tx_pack,
            "tx_bytes": tx_bytes,
            "tx_err": tx_err,
            "tx_drop": tx_drop,
            "bit_rate": self.bit_rate
        }

##############################################################################
#                               Aux Functions                                #
##############################################################################

def gen_iface(raw_data: dict[str, int]) -> IfaceInfo:
    """Generate a IfaceInfo object from a dictionary"""
    return IfaceInfo(
        rx_pack  = raw_data.get("rx_pack", -1),
        rx_bytes = raw_data.get("rx_bytes", -1),
        rx_err   = raw_data.get("rx_err", -1),
        rx_drop  = raw_data.get("rx_drop", -1),
        tx_pack  = raw_data.get("tx_pack", -1),
        tx_bytes = raw_data.get("tx_bytes", -1),
        tx_err   = raw_data.get("tx_err", -1),
        tx_drop  = raw_data.get("tx_drop", -1)
    )

##############################################################################
#                              Public Functions                              #
##############################################################################

async def read_net_info() -> dict[str, IfaceInfo]:
    """Read the system network interfaces information and return in dictionary format,
    in kbi parsed to integer.
    
    Will return and empty dict if any error is found"""
    ifaces: dict[str, IfaceInfo] = {}

    try:
        raw_ifaces_data: dict[str, int] = await infra_files.get_net_info()

        for iface in raw_ifaces_data:
            # Enrich iface data with other datasource data (iwconfig)
            extra_data: dict[str, str] = await infra_cmd.get_net_info(iface)
            raw_ifaces_data[iface].update(extra_data)

            ifaces[iface] = gen_iface(raw_ifaces_data[iface])

    except Exception as err:
        logging.warning("Unexpected error:\n%s", err)

    return ifaces
