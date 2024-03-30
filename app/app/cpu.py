"""Defines the app level functions for CPU"""
import logging

if __name__ == "__main__" or \
    __name__.startswith("domain") or \
    __name__.startswith("app.app."):
    from app.domain import cpu as domain_cpu

elif __name__.startswith("tests."):
    from tests.domain import cpu as domain_cpu

else:
    logging.error("Unexpected module load: %s", __name__)
    exit(1)

##############################################################################
#                              Public Functions                              #
##############################################################################

async def read_cpu_info() -> dict:
    """Read the system CPU Load information and return in dictionary format,
    parsed to float. Ready to be returned as API response.
    
    Will return -1 for each load average if any error is found"""
    return await domain_cpu.read_cpu_info()
