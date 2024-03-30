"""Defines the app level functions for Memory"""
import logging

if __name__ == "__main__" or \
    __name__.startswith("domain") or \
    __name__.startswith("app.app."):
    from app.domain import memory as domain_mem

elif __name__.startswith("tests."):
    from tests.domain import memory as domain_mem

else:
    logging.error("Unexpected module load: %s", __name__)
    exit(1)

##############################################################################
#                              Public Functions                              #
##############################################################################

async def read_ram_info() -> dict:
    """Read the system Memory information and return in dictionary format,
    in kbi parsed to integer.
    
    Will return -1 for each memory amount if any error is found"""
    return await domain_mem.read_ram_info()
