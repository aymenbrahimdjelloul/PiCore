"""
This code or file is pertinent to the 'PiCore' Project
Copyright (c) 2024, 'Aymen Brahim Djelloul'. All rights reserved.
Use of this source code is governed by a MIT license that can be
found in the LICENSE file.


@author : Aymen Brahim Djelloul
Version : 1.0.0
Date : 29.08.2024
License : MIT




    // SOURCES : 
        - https://www.raspberrypi.com/documentation/computers/raspberry-pi.html
        - https://www.raspberrypi.com/documentation/computers/configuration.html
        - https://www.raspberrypi.com/documentation/computers/config_txt.html
        - https://www.raspberrypi.com/products/raspberry-pi-5/
"""

# IMPORTS
import sys
import subprocess
import os.path
from utils import *
from const import *
from exceptions import *


# Define if running on supported platform
if get_system_id() not in SUPPORTED_PLATFORMS:
    raise NotSUpportedPlatform(PLATFORM, SUPPORTED_PLATFORMS)


class PiCore:

    def __init__(self, debug_mode: bool = False) -> None:
        
        self.debug_mode = debug_mode
        
        # Check if running on a virtual machine
        if is_virtual_machine() and self.debug_mode:
            # Raise Running Vm error
            raise RunningOnVirtualMachine()
        
        # load 'config.txt file if exist'
        self.config: str = open(CONFIG_FILE, 'r').read() if os.path.isfile(CONFIG_FILE) else None

        # Check if running on raspberrypi
        self.is_raspberrypi: bool = is_raspberrypi()

        # Check for 'vcgencmd' if exists

    def _get_command_output(self, command: list) -> str:
        """ This method will get the output of a specefic command using subprocess """
        return subprocess.check_output(command, text=True)
    
    def _get_query_data(self, pattern: str) -> str:
        """ This method will get data from string text according to query"""

        # First method: Using 'lscpu'
        if self.lscpu_data:
            for line in self.lscpu_data.splitlines():
                if line.startswith(pattern):
                    return line.split(':', 1)[1].strip()
                
        # Second method: Using 'cat /proc/cpuinfo'
        if self.cpuinfo_data:
            for line in self.cpuinfo_data.splitlines():
                if line.startswith(pattern):
                    return line.split(':', 1)[1].strip()
                
        # Other-wise return None
        else:
            return None
        
    # def _is_vcgencmd_exist(self) -> bool:
    #     """ This method will check if vcgncmd raspberry pi manager program exists """
    #     return True if self._get_command_output(CHECK_VCGENCMD) != "" else False
    
    def _is_config_enabled(self, config_string: str) -> bool:
        """ This method will check if a config is enabled or not using 
            the configuration string pattern """

        try:
            _config: str = open(CONFIG_FILE, 'r').read()

            for line in _config.splitlines():

                if config_string in line:
                    if line.startswith("#"):
                        return False
                    else:
                        return True

        except FileNotFoundError:
            return None

        else:
            return None
        
    def _extract_value(self, pattern: str, string: str) -> str:
        """ This method will get specific value from a given string"""

        # Iterate through every line
        for line in string.splitlines():
            
            string: str = line.strip("#=")
            print(string)
            if string.startswith(pattern):
                return string[len(pattern): len(string)]
        
        # Other-wise retrun None
        return None

class Pi(PiCore):

    def __init__(self) -> None:
        super(Pi, self).__init__()


    def pi_model(self) -> str:
        """ This method will get the Raspberry Pi Model name string !"""
        # NOT YET
        return ""

    def serial_number(self) -> str:
        """ This method will get the Raspberry Pi internal serial number !
        SOURCE : https://www.raspberrypi.com/documentation/computers/config_txt.html#the-serial-number-filter """

        if self.is_raspberrypi:
            try:
                # Read the serial number from /proc/cpuinfo
                with open(CPUINFO, 'r') as f:
                    cpuinfo = f.read()
                
                # Extract the serial number
                for line in cpuinfo.splitlines():
                    if line.startswith('Serial'):
                        serial = line.split(':')[1].strip()
                        return serial
                
                # If Serial not found
                return None

            except FileNotFoundError:
                return None
            
        else:
            return None
        

class Processor(PiCore):

    def __init__(self) -> None:
        super(Processor, self).__init__()

        # request CPU data
        self.lscpu_data: str = self._get_command_output([LSCPU])
        self.cpuinfo_data: str = self._get_command_output(CPUINFO)


    def name(self) -> str:
        """ This method will get the cpu name string """

        return self._get_query_data("Model name:")

    def archeticture(self) -> str:
        """ This method will get the cpu archeticture string name """

        return self._get_query_data("Architecture:")

    def stepping(self) -> int:
        """ This method will get the cpu Stepping value """

        return self._get_query_data("Stepping:")

    def family(self) -> int:
        """ This method will get the cpu Family value """

        return self._get_query_data("CPU family:")

    def cores_count(self, logical=False) -> int:
        """ This method will get the cores and threads number on the cpu """

        return int(self._get_query_data("Thread(s) per core:")) * int(self._get_query_data("CPU(s):")) \
                if logical else self._get_query_data("CPU(s):")

    def max_clock_speed(self, aliased: bool = True) -> float:
        """ This method will get the maximum cpu clock speed """

        return mhz_to_ghz(float(self._get_query_data("CPU MHz:"))) if aliased else \
                float(self._get_query_data("CPU MHz:"))

    def base_clock_speed(self, aliased: bool = True) -> float:
        """ This method will get the maximum cpu clock speed """

        # Method 1 : using cpu data to get the proper
        # base clock speed value
        cpu_name: str = self.name()

        # Check the model name validity
        if cpu_name:
            # Handle exceptions
            try:
                # Get the value from the json dictionary
                return mhz_to_ghz(CPU_DATA[cpu_name]["base_clock_speed"]) if aliased else \
                        CPU_DATA[cpu_name]["base_clock_speed"]
            
            except KeyError:
                pass

        # Clear memory
        del cpu_name

        # Method 2 : Calculate mathematically the cpu
        # base clock speed using max clock speed and scaling factor
        return mhz_to_ghz(self.max_clock_speed(aliased=False) / SCALING_FACTOR) if aliased else \
                self.max_clock_speed(aliased=False) / SCALING_FACTOR

    def l1i_cache_size(self, aliased: bool = True) -> int:
        """ This method will get the level 1 instructions cache size"""

        return self._get_query_data("L1i cache:") if aliased else \
                kb_to_bytes(self._get_query_data("L1i cache:"))

    def l1d_cache_size(self, aliased: bool = True) -> int:
        """ This method will get the level 1 data cache size """

        return self._get_query_data("L1d cache:") if aliased else \
            kb_to_bytes(self._get_query_data("L1d cache:"))

    def l2_cache_size(self, aliased: bool = True) -> int:
        """ This method will get the level 2 cache memory size on cpu """

        return self._get_query_data("L2 cache:") if aliased else \
            mb_to_bytes(self._get_query_data("L2 cache:"))

    def l3_cache_size(self, aliased: bool = True) -> int:
        """ This method will get the level 3 cache memory size on cpu """

        return self._get_query_data("L3 cache:") if aliased else \
            mb_to_bytes(self._get_query_data("L3 cache:"))

    def is_overclock(self) -> bool:
        """ This method will get the cpu is overclocked or not 
            SOURC : https://www.raspberrypi.com/documentation/computers/config_txt.html#overclocking """
        
        return True if self._is_config_enabled("over_voltage") else False

    def is_force_turbo(self) -> bool:
        """ This method will get if the raspberry pi is forced turbo 
            SOURCE : https://www.raspberrypi.com/documentation/computers/config_txt.html#overclocking """
        
        return True if self._is_config_enabled("force_turbo") else False

    def voltage(self) -> float:
        """ This method will get the cpu regular voltage """
        
        # Check if running on a raspberry pi
        if self.is_raspberrypi:

            # Check if the cpu is not overclocked
            if self.is_overclock():
                # Method 1 : if the cpu is overclocked use 'config.txt' to get voltage
                return float(self._extract_value("over_voltage", self.config))

            else:
                # Method 2: if the not overclocked use pre-colletcted data 
                # to get the specefic cpu voltage
                cpu_name: str = self.name()     

                # CHeck cpu name validity
                if cpu_name and not is_virtual_machine():
                    # return the cpu voltage from json data
                    return CPU_DATA[cpu_name]["voltage"]

        # Other-wise return 1.2 v as the default voltage for all ARM cpus
        return 1.2

    def release_date(self) -> str:
         """ This method will return the cpu release date string"""
         return CPU_DATA[self.name()]["release_date"] if self.is_raspberrypi else None
    
    def flags(self) -> list:
        """ This method will get the cpu flags in list"""
        return self._get_query_data("Flags:").split()


class Sensors(PiCore):

    def __init__(self) -> None:
        super(Sensors, self).__init__()

    def current_clock_speed(self) -> float:
        """ This method will get the current sesnor readings cpu clock speed"""

    def get_current_temp(self) -> float:
        """ This method will current sensor thermal readings or estimated"""

    def get_current_voltage(self) -> float:
        """ This method will get current cpu voltage sensors reading"""


if __name__ == "__main__":
    sys.exit()
