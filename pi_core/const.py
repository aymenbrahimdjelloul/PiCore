# This code or file is pertinent to the 'PiCore' Project
# Copyright (c) 2024, 'Aymen Brahim Djelloul'. All rights reserved.
# Use of this source code is governed by a MIT license that can be
# found in the LICENSE file.

# Author : Aymen Brahim DJelloul
# Version : 1.0.0
# Date : 29.08.2024
# License : MIT

# IMPORTS
import sys
import json
import platform

# DEFINE BASIC VARIABLES
AUTHOR: str = "Aymen Brahim Djelloul"
VERSION: str = "1.0.0"
LICENSE: str = "MIT"

# DEFINE PLATFORM SYSTEM VARIABLES
PLATFORM: str = platform.system()
SUPPORTED_PLATFORMS: tuple = ('debian', 'Ubuntu', 'linuxmint')

# DEIFNE SYSTEM FILES PATHS
CONFIG_FILE: str = "/boot/config.txt"
OS_RELEASE: str = "/etc/os-release"
CPUINFO: str = ["cat", "/proc/cpuinfo"]
CHECK_VCGENCMD: str = ["which", "vcgencmd"]
LSCPU: str = "lscpu"

# LOAD JSON FILE DATA
CPU_DATA: dict = json.loads(open('cpu_data.json', 'r').read())

# DEFINE CPU VAIRIABLES
SCALING_FACTOR: float = 1.6


if __name__ == "__main__":
    sys.exit()
