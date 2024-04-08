"""
This module contains the tests for the App layer
"""
import unittest
from unittest.mock import patch

import context

class TestAppLayer(unittest.IsolatedAsyncioTestCase):
    """
    This class contains the tests for the App layer
    """

    @patch('context.app.domain.cpu.read_cpu_info')
    async def test_read_cpu_info(self, mock_read_cpu_info):
        """
        This method tests read cpu info function
        """

        expected_keys: list[str] = ["m1", "m5", "m15"]

        async def read_cpu_info_mock() -> context.app.domain.cpu.CPULoadAvgs:
            cpu_data: context.app.domain.cpu.CPULoadAvgs = context.app.domain.cpu.CPULoadAvgs()
            
            cpu_data.m1 = 1
            cpu_data.m5 = 1.1
            cpu_data.m15 = 2

            return cpu_data

        mock_read_cpu_info.side_effect = read_cpu_info_mock

        raw_cpu_data: str = str(await context.app.app.cpu.read_cpu_info())

        for key in expected_keys:
            assert key in raw_cpu_data

    @patch('context.app.domain.memory.read_ram_info')
    async def test_read_mem_info(self, mock_read_memory_info):
        """
        This method tests read memory info function
        """
        async def read_memory_info_mock(unit: str = "B") -> context.app.domain.memory.RAMRawInfo:
            unit_order: int = 1
            units: list[str] = ["B", "kB", "MB", "GB"]
            if unit in units:
                unit_order += units.index(unit)
            ram_raw: dict[str, int] = {
                "mem_total": 100 * (1024 ** unit_order),
                "mem_free": 95 * (1024 ** unit_order),
                "mem_ava": 95 * (1024 ** unit_order),
                "mem_used": 5 * (1024 ** unit_order)
            }
            ram: context.app.domain.memory.RAMRawInfo = context.app.domain.memory.RAMRawInfo()
            ram.mem_total = ram_raw['mem_total']
            ram.mem_free = ram_raw['mem_free']
            ram.mem_ava = ram_raw['mem_ava']

            return ram

        mock_read_memory_info.side_effect = read_memory_info_mock
        units: list[str] = ["B", "kB", "MB", "GB"]
        expected_keys: list[str] = ["total", "free", "ava", "used"]

        for unit in units:
            raw_memory_data = await context.app.app.memory.read_ram_info(unit)
            for key in expected_keys:
                assert key in raw_memory_data

    @patch('context.app.domain.disk.read_disks_info')
    async def test_read_disks_info(self, mock_read_disks_info):
        """
        This method tests read disks info function
        """
        async def read_disks_info_mock(unit: str = "B") -> dict[str, context.app.domain.disk.DeviceInfo]:
            unit_order: int = 1
            units: list[str] = ["B", "kB", "MB", "GB"]
            if unit in units:
                unit_order += units.index(unit)
            disk_raw: dict[str, context.app.domain.disk.DeviceInfo] = {
                "sda": context.app.domain.disk.DeviceInfo(
                    partitions={
                        "sda1": context.app.domain.disk.PartitionInfo(
                            mount_point="/",
                            total=100 * (1024 ** unit_order),
                            used=5 * (1024 ** unit_order),
                            free=95 * (1024 ** unit_order)
                        ),
                        "sda2": context.app.domain.disk.PartitionInfo(
                            mount_point="/boot",
                            total=10 * (1024 ** unit_order),
                            used=1 * (1024 ** unit_order),
                            free=9 * (1024 ** unit_order)
                        )
                    }
                ),
                "sdb": context.app.domain.disk.DeviceInfo(
                    partitions={
                        "sdb1": context.app.domain.disk.PartitionInfo(
                            mount_point="/mnt/data",
                            total=200 * (1024 ** unit_order),
                            used=10 * (1024 ** unit_order),
                            free=190 * (1024 ** unit_order)
                        ),
                        "sdb2": context.app.domain.disk.PartitionInfo(
                            mount_point="/mnt/data2",
                            total=100 * (1024 ** unit_order),
                            used=1 * (1024 ** unit_order),
                            free=99 * (1024 ** unit_order)
                        )
                    }
                )
            }

            return disk_raw

        mock_read_disks_info.side_effect = read_disks_info_mock
        units: list[str] = ["B", "kB", "MB", "GB"]
        expected_keys: list[str] = ["total", "used", "free", "mount_point"]

        for unit in units:
            raw_disk_data = await context.app.app.disk.read_disks_info(unit)
            for disk_name, disk_data in raw_disk_data.items():
                for partition_name, partition_data in disk_data['partitions'].items():
                    for key in expected_keys:
                        assert key in partition_data

    @patch('context.app.domain.network.read_net_info')
    async def test_read_network_info(self, mock_read_network_info):
        """
        This method tests read network info function
        """
        async def read_network_info_mock(unit: str = "B") -> dict[str, context.app.domain.network.IfaceInfo]:
            unit_order: int = 1
            units: list[str] = ["B", "kB", "MB", "GB"]
            if unit in units:
                unit_order += units.index(unit)

            net_raw: dict[str, context.app.domain.network.IfaceInfo] = {
                "eth0": context.app.domain.network.IfaceInfo(),
                "wlan0": context.app.domain.network.IfaceInfo()
            }
            
            mock_read_network_info.side_effect = read_network_info_mock
            units: list[str] = ["B", "kB", "MB", "GB"]
            expected_keys: list[str] = [ 
                "rx_pack", "rx_bytes", "rx_err",
                "rx_drop", "tx_pack", "tx_bytes",
                "tx_err", "tx_drop", "bit_rate"
            ]

            for unit in units:
                raw_network_data = await context.app.app.network.read_net_info(unit)
                for iface_name, iface_data in raw_network_data.items():
                    for key in expected_keys:
                        assert key in iface_data
