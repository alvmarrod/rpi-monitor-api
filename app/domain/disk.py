"""Defines data model and domain entities for Disk domain"""
import re
import json
import logging
import dataclasses as dc
from typing import Union

import app.infrastructure.cmd as infra_cmd

###############################################################################
#                                Data Model                                  #
###############################################################################

@dc.dataclass
class PartitionInfo:
    """Models Disk Partition Information. Storage unit is bytes"""
    mount_point : str = ""
    fs_type     : str = ""
    total       : int = -1
    used        : int = -1
    free        : int = -1

    def __str__(self) -> str:
        """Overwrite class representation"""
        return json.dumps(self.as_dict())

    def as_dict(self, unit: str = "B") -> dict:
        """Return the class as a dictionary. The unit can be changed"""

        unit_order: int = 1
        available_units: list[str] = ["B", "kB", "MB", "GB"]

        if unit in available_units:
            unit_order += available_units.index(unit)

        total_gb = self.total / (1024 ** unit_order)
        used_gb = self.used / (1024 ** unit_order)
        free_gb = self.free / (1024 ** unit_order)
        return {
            "mount_point": self.mount_point,
            "fs_type": self.fs_type,
            "total": total_gb,
            "used": used_gb,
            "free": free_gb
        }

@dc.dataclass
class DeviceInfo:
    """Models Disk Device Information.
    The key for the partitions dictionary is the mount point."""
    device      : str = ""
    partitions  : dict[str, PartitionInfo] = dc.field(default_factory=dict)

    def __str__(self) -> str:
        """Overwrite class representation"""
        return json.dumps(self.as_dict())
    
    def as_dict(self, unit: str = "B") -> dict:
        """Return the class as a dictionary. The unit can be changed"""
        partitions: dict[str, dict] = {}
        for key, value in self.partitions.items():
            partitions[key] = value.as_dict(unit)

        return {
            "device": self.device,
            "partitions": partitions
        }

###############################################################################
#                               Aux Functions                                #
###############################################################################

def _get_base_device_name(device_name: str) -> str:
    """Return the base device name from a device name"""
    match = re.match(r"(/dev/\D+)", device_name)
    if match:
        return match.group(1)
    else:
        return device_name

def gen_partition(dev_data: dict[str, str]) -> PartitionInfo:
    """Parse the device information from a dictionary to a DeviceInfo object"""
    partition: PartitionInfo = PartitionInfo()

    partition.mount_point = dev_data['mount']
    # partition.fs_type = dev_data['fs_type']
    partition.total = dev_data['total']
    partition.used = dev_data['used']
    partition.free = dev_data['free']

    return partition

###############################################################################
#                              Public Functions                              #
###############################################################################

async def read_disks_info() -> dict[DeviceInfo]:
    """Read the system disks information and return in dictionary format.
    
    Will return an empty dict if any error is found"""
    devices: dict[DeviceInfo] = {}

    try:
        raw_filesystem_data: dict[str, dict[str, Union[int, str]]] = \
            infra_cmd.get_disk_usage()

        for device, dev_data in raw_filesystem_data.items():
            base_device = _get_base_device_name(device)
            if base_device not in devices:
                devices[base_device] = DeviceInfo()
                devices[base_device].device = base_device
            
            partititon: PartitionInfo = gen_partition(dev_data)
            devices[base_device].partitions[partititon.mount_point] = partititon

    except Exception as err:
        logging.error("Unexpected error reading disk info:\n%s", str(err))

    return devices
