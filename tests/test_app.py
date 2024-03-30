"""
This module contains the tests for the App layer
"""
import logging
import unittest
from unittest.mock import MagicMock, patch

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

        async def read_cpu_info_mock():
            return {"m1": float(1), "m5": float(1.1), "m15": float(2)}

        mock_read_cpu_info.side_effect = read_cpu_info_mock

        raw_cpu_data: str = str(await context.app.app.cpu.read_cpu_info())

        for key in expected_keys:
            assert key in raw_cpu_data

    @patch('context.app.domain.memory.read_ram_info')
    async def test_read_memoryinfo(self, mock_read_memory_info):
        """
        This method tests read memory info function
        """

        expected_keys: list[str] = ["mem_total", "mem_free", "mem_ava", "mem_used"]

        async def read_memory_info_mock():
            return {"mem_total": 100, "mem_free": 95, "mem_ava": 95, "mem_used": 5}

        mock_read_memory_info.side_effect = read_memory_info_mock

        raw_memory_data = str(await context.app.app.memory.read_ram_info())

        for key in expected_keys:
            assert key in raw_memory_data
