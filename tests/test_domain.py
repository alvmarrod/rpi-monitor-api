"""
This module contains the tests for the Domain layer
"""
import unittest
from typing import Union
from unittest.mock import patch

import context

class TestDomainLayer(unittest.IsolatedAsyncioTestCase):
    """
    This class contains the tests for the Domain layer
    """

    @patch('context.app.infrastructure.files.get_cpu_load_avg')
    @patch('context.app.infrastructure.files.get_cpu_cores')
    async def test_read_cpu_info(self, mock_get_cpu_cores, mock_get_cpu_load_avg):
        """
        This method tests read cpu info function
        """

        # Usage is returned in percentage
        expected: dict[str, int] = {"m1": 25, "m5": 12.5, "m15": 10.75}

        async def get_cpu_cores() -> int:
            return 4

        async def get_cpu_load_avg() -> dict[str, str]:
            return {"1m": "1", "5m": "0.5", "15m": "0.43"}

        mock_get_cpu_cores.side_effect = get_cpu_cores
        mock_get_cpu_load_avg.side_effect = get_cpu_load_avg

        cpu: context.app.domain.cpu.CPULoadAvgs = await context.app.domain.cpu.read_cpu_info()

        assert cpu.m1 == expected['m1'], f"Unexpected m1 value: {cpu.m1}"
        assert cpu.m5 == expected['m5'], f"Unexpected m5 value: {cpu.m5}"
        assert cpu.m15 == expected['m15'], f"Unexpected m15 value: {cpu.m15}"

    @patch('context.app.infrastructure.files.get_mem_info')
    async def test_read_ram_info(self, mock_read_memory_info):
        """
        This method tests read memory info function
        """

        expected: dict[str, int] = {
            "mem_total": 100 * 1024,
            "mem_free": 95 * 1024,
            "mem_ava": 95 * 1024,
            "mem_used": 5 * 1024
        }

        async def read_memory_info_mock() -> dict[str, int]:
            """File information mock is in kB"""
            return {"mem_total": 100, "mem_free": 95, "mem_ava": 95}

        mock_read_memory_info.side_effect = read_memory_info_mock

        ram: context.app.domain.memory.RAMRawInfo = await context.app.domain.memory.read_ram_info()

        assert ram.mem_total == expected['mem_total'], f"Unexpected mem_total value: {ram.mem_total}"
        assert ram.mem_free == expected['mem_free'], f"Unexpected mem_free value: {ram.mem_free}"
        assert ram.mem_ava == expected['mem_ava'], f"Unexpected mem_ava value: {ram.mem_ava}"
        assert ram.mem_used == expected['mem_used'], f"Unexpected mem_used value: {ram.mem_used}"

    @patch('context.app.infrastructure.cmd.get_disk_usage')
    async def test_read_disks_info(self, mock_read_disks_info):
        """
        This method tests read disks info function
        """

        disk_mock: dict[str, dict[str, Union[int, str]]] = {
                'none': {
                    'total': 3897556, 
                    'used': 524, 
                    'free': 3897032, 
                    'mount': '/mnt/wslg/doc'
                },
                '/dev/sdc': {
                    'total': 263112772,
                    'used': 13456428,
                    'free': 236218188,
                    'mount': '/'
                },
                'rootfs': {
                    'total': 3894296,
                    'used': 1884,
                    'free': 3892412,
                    'mount': '/init'
                },
                'tmpfs': {
                    'total': 3897556,
                    'used': 0,
                    'free': 3897556,
                    'mount': '/sys/fs/cgroup'
                },
                'C:\\': {
                    'total': 999138300,
                    'used': 891378584,
                    'free': 107759716,
                    'mount': '/mnt/c'
                }
            }

        def read_disks_info_mock() -> dict[str, dict[str, Union[int, str]]]:
            """File information mock is in kB"""
            return disk_mock

        mock_read_disks_info.side_effect = read_disks_info_mock

        disks: dict[str, context.app.domain.disk.DeviceInfo] = await context.app.domain.disk.read_disks_info()

        assert len(disks) == len(disk_mock), f"Unexpected number of devices: {len(disks)}"
        for device, dev_data in disk_mock.items():
            dev_partition: context.app.domain.disk.PartitionInfo = disks[device].partitions[dev_data['mount']]
            assert device in disks, f"Device {device} not found in disks"
            assert disks[device].device == device, f"Unexpected device name: {disks[device].device}"
            assert len(disks[device].partitions) == 1, f"Unexpected number of partitions: {len(disks[device].partitions)}"
            assert dev_partition.total == dev_data['total'], f"Unexpected total value: {dev_partition.total}"
            assert dev_partition.used == dev_data['used'], f"Unexpected used value: {dev_partition.used}"
            assert dev_partition.free == dev_data['free'], f"Unexpected free value: {dev_partition.free}"
            assert dev_partition.mount_point == dev_data['mount'], f"Unexpected mount point value: {dev_partition.mount_point}"

    @patch('context.app.infrastructure.files.get_net_info')
    @patch('context.app.infrastructure.cmd.get_net_info')
    async def test_read_net_info(self, mock_get_net_info_cmd, mock_get_net_info):
        """
        This method tests read network info function
        """

        net_mock: dict[str, context.app.domain.network.IfaceInfo] = {
            'eth0': {
                'rec_pack': 100,
                'rec_bytes': 1024,
                'rec_err': 1,
                'rec_drop': 2,
                'snd_pack': 200,
                'snd_bytes': 2048,
                'snd_err': 3,
                'snd_drop': 4,
                'bit_rate': '1 Gb/s'
            },
            'wlan0': {
                'rec_pack': 300,
                'rec_bytes': 3072,
                'rec_err': 5,
                'rec_drop': 6,
                'snd_pack': 400,
                'snd_bytes': 4096,
                'snd_err': 7,
                'snd_drop': 8,
                'bit_rate': '100 Mb/s'
            }
        }

        statistics_keys: list[str] = [
            'rec_pack', 'rec_bytes', 'rec_err', 'rec_drop',
            'snd_pack', 'snd_bytes', 'snd_err', 'snd_drop'
        ]

        link_keys: list[str] = ['bit_rate']

        async def get_net_info_mock() -> dict[str, int]:
            """Interface list information mock"""
            return {
                'eth0': {key: val for key, val in net_mock['eth0'].items() if key in statistics_keys},
                'wlan0': {key: val for key, val in net_mock['wlan0'].items() if key in statistics_keys}
            }

        async def get_net_info_cmd_mock(iface: str) -> dict[str, str]:
            """iwconfig interface data mock"""
            return {key: val for key, val in net_mock[iface].items() if key in link_keys}

        mock_get_net_info.side_effect = get_net_info_mock
        mock_get_net_info_cmd.side_effect = get_net_info_cmd_mock

        net: dict[str, context.app.domain.network.IfaceInfo] = await context.app.domain.network.read_net_info()

        for iface, iface_data in net_mock.items():
            assert iface in net, f"Interface {iface} not found in net"
            for key in statistics_keys:
                assert iface_data[key] == net_mock[iface][key], f"Unexpected value for {key} in {iface}"
            for key in link_keys:
                assert iface_data[key] == net_mock[iface][key], f"Unexpected value for {key} in {iface}"