"""
This module contains the tests for the Infrastructure layer
"""
import unittest
from unittest.mock import patch, mock_open

import context

class TestInfrastructureLayer(unittest.IsolatedAsyncioTestCase):
    """
    This class contains the tests for the Infrastructure layer
    """

    @patch("builtins.open")
    async def test_get_cpu_cores(self, open_mock):
        """
        This method tests read cpu info function
        """

        cpu_info_file: str = """processor       : 0
model name      : ARMv7 Processor rev 4 (v7l)
BogoMIPS        : 38.40
Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xd03
CPU revision    : 4

processor       : 1
model name      : ARMv7 Processor rev 4 (v7l)
BogoMIPS        : 38.40
Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xd03
CPU revision    : 4

processor       : 2
model name      : ARMv7 Processor rev 4 (v7l)
BogoMIPS        : 38.40
Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xd03
CPU revision    : 4

processor       : 3
model name      : ARMv7 Processor rev 4 (v7l)
BogoMIPS        : 38.40
Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xd03
CPU revision    : 4

Hardware        : BCM2835
Revision        : a02082
Serial          : XXXXXXXXXXXXXXXX
Model           : Raspberry Pi 3 Model B Rev 1.2"""

        open_mock.side_effect = mock_open(read_data=cpu_info_file)

        cores: int = await context.app.infrastructure.files.get_cpu_cores()

        assert cores == 4, f"Unexpected cores, value: {cores}"

    @patch("builtins.open")
    async def test_get_cpu_load_avg(self, open_mock):
        """
        This method tests read cpu load avg function
        """

        # Usage is returned in percentage
        expected: dict[str, int] = {"1m": "0.53", "5m": "0.60", "15m": "0.62"}

        cpu_load_file: str = "0.53 0.60 0.62 1/156 27996"
        open_mock.side_effect = mock_open(read_data=cpu_load_file)

        load: dict[str, int] = await context.app.infrastructure.files.get_cpu_load_avg()

        for key, value in expected.items():
            assert load[key] == value, f"Unexpected value for {key}, value: {load[key]}"

    @patch("builtins.open")
    async def test_get_mem_info(self, open_mock):
        """
        This method tests read mem function
        """

        expected: dict[str, int] = {"mem_total": 945364, "mem_free": 163000, "mem_ava": 717680}

        mem_info_file: str = """MemTotal:         945364 kB
MemFree:          163000 kB
MemAvailable:     717680 kB
Buffers:           70396 kB
Cached:           541668 kB
SwapCached:          220 kB
Active:           231872 kB
Inactive:         475848 kB
Active(anon):        636 kB
Inactive(anon):   124792 kB
Active(file):     231236 kB
Inactive(file):   351056 kB
Unevictable:          16 kB
Mlocked:              16 kB
SwapTotal:        204796 kB
SwapFree:         191228 kB
Dirty:                 0 kB
Writeback:             0 kB
AnonPages:         95652 kB
Mapped:           116204 kB
Shmem:             29772 kB
KReclaimable:      34884 kB
Slab:              55856 kB
SReclaimable:      34884 kB
SUnreclaim:        20972 kB
KernelStack:        1272 kB
PageTables:         1880 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:      677476 kB
Committed_AS:     549136 kB
VmallocTotal:    1114112 kB
VmallocUsed:        4724 kB
VmallocChunk:          0 kB
Percpu:             1456 kB
CmaTotal:          65536 kB
CmaFree:           15444 kB"""
        open_mock.side_effect = mock_open(read_data=mem_info_file)

        mem: dict[str, int] = await context.app.infrastructure.files.get_mem_info()

        for key, value in expected.items():
            assert mem[key] == value, f"Unexpected value for {key}, value: {mem[key]}"
