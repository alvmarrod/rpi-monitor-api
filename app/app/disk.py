"""Defines the app level functions for Disk/Storage"""
import logging

if __name__ == "__main__" or \
    __name__.startswith("domain") or \
    __name__.startswith("app.app."):
    from app.domain import disk as domain_disk

elif __name__.startswith("tests."):
    from tests.domain import disk as domain_disk

else:
    logging.error("Unexpected module load: %s", __name__)
    exit(1)

###############################################################################
#                              Public Functions                              #
###############################################################################

async def read_disks_info(unit: str) -> dict:
    """Read the system storage information and return in dictionary format,
    in kbi parsed to integer.
    
    Will return an empty dict if any error is found"""
    disks: dict[str, domain_disk.DeviceInfo] = await domain_disk.read_disks_info()
    return {device: disk.as_dict(unit) for device, disk in disks.items()}
