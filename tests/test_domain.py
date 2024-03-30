"""
This module contains the tests for the Domain layer
"""
import logging
import unittest
from unittest.mock import MagicMock, patch

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

        async def get_cpu_cores():
            return 4

        async def get_cpu_load_avg():
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

        expected: dict[str, int] = {"mem_total": 100, "mem_free": 95, "mem_ava": 95, "mem_used": 5}

        async def read_memory_info_mock():
            return {"mem_total": 100, "mem_free": 95, "mem_ava": 95}

        mock_read_memory_info.side_effect = read_memory_info_mock

        ram: context.app.domain.memory.RAMRawInfo = await context.app.domain.memory.read_ram_info()

        assert ram.mem_total == expected['mem_total'], f"Unexpected mem_total value: {ram.mem_total}"
        assert ram.mem_free == expected['mem_free'], f"Unexpected mem_free value: {ram.mem_free}"
        assert ram.mem_ava == expected['mem_ava'], f"Unexpected mem_ava value: {ram.mem_ava}"
        assert ram.mem_used == expected['mem_used'], f"Unexpected mem_used value: {ram.mem_used}"
