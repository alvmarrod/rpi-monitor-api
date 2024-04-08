"""Defines the app level functions for Network"""
import logging

if __name__ == "__main__" or \
    __name__.startswith("domain") or \
    __name__.startswith("app.app."):
    from app.domain import network as domain_net

elif __name__.startswith("tests."):
    from tests.domain import network as domain_net

else:
    logging.error("Unexpected module load: %s", __name__)
    exit(1)

##############################################################################
#                              Public Functions                              #
##############################################################################

async def read_net_info(unit: str) -> dict:
    """Read the system networking information and return in dictionary format
    
    Will return an empty dictionary if any error is found"""
    net: dict[str, domain_net.IfaceInfo] = await domain_net.read_net_info()
    return net.as_dict(unit)
