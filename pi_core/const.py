# Author : Aymen Brahim DJelloul
# Version : 1.0
# Date : 29.08.2024
# License : MIT

# IMPORTS
import sys
import json
import platform

# DEFINE BASIC VARIABLES
AUTHOR: str = "Aymen Brahim Djelloul"
VERSION: str = "1.0"
LICENSE: str = "MIT"

# DEFINE PLATFORM SYSTEM VARIABLES
PLATFORM: str = platform.system()
SUPPORTED_PLATFORMS: tuple = ('debian', 'Ubuntu', 'linuxmint')

# DEIFNE SYSTEM FILES PATHS
OS_RELEASE: str = "/etc/os-release"
CPUINFO: str = ["cat", "/proc/cpuinfo"]
LSCPU: str = "lscpu"

# LOAD JSON FILE DATA
CPU_DATA: dict = json.loads(open('data.json', 'r').read())

# DEFINE CPU VAIRIABLES
SCALING_FACTOR: float = 1.6


if __name__ == "__main__":
    sys.exit()
