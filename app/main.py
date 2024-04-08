"""App main module"""

import logging
from typing import Optional
from fastapi import FastAPI, Query

import app.app.cpu as app_cpu
import app.app.memory as app_mem
import app.app.disk as app_disk
import app.app.network as app_net

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

rpi_mon_api: FastAPI = FastAPI()

@rpi_mon_api.get("/")
async def root():
    return {"message": "Not implemented"}

@rpi_mon_api.get("/v1/cpu")
async def cpu_avg():
    """Read the system CPU Load information and return in dictionary format,
    parsed to float. Ready to be returned as API response.
    
    Will return -1 for each load average if any error is found"""
    return await app_cpu.read_cpu_info()

@rpi_mon_api.get("/v1/mem")
async def ram_info(unit: Optional[str] = Query('kB')):
    """Read the system Memory information and return in dictionary format.
    
    Will return -1 for each memory amount if any error is found"""
    return await app_mem.read_ram_info(unit)

@rpi_mon_api.get("/v1/disk")
async def disk_info(unit: Optional[str] = Query('kB')):
    """Read the system storage information and return in dictionary format.
    
    Will return an empty dict if any error is found"""
    return await app_disk.read_disks_info(unit)

@rpi_mon_api.get("/v1/net")
async def net_info(unit: Optional[str] = Query('kB')):
    """Read the system network interfaces information and return in dictionary
    format.
    
    Will return an empty dict if any error is found"""
    return await app_net.read_net_info(unit)
