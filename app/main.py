"""App main module"""

import logging
from fastapi import FastAPI

import app.app.cpu as app_cpu
import app.app.memory as app_mem

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

rpi_mon_api: FastAPI = FastAPI()

@rpi_mon_api.get("/")
async def root():
    return {"message": "Hello World"}

@rpi_mon_api.get("/v1/cpuavg")
async def cpu_avg():
    """Read the system CPU Load information and return in dictionary format,
    parsed to float. Ready to be returned as API response.
    
    Will return -1 for each load average if any error is found"""
    return await app_cpu.read_cpu_info()

@rpi_mon_api.get("/v1/raminfo")
async def ram_info():
    """Read the system Memory information and return in dictionary format,
    in kbi parsed to integer.
    
    Will return -1 for each memory amount if any error is found"""
    return await app_mem.read_ram_info()
