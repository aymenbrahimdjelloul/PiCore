"""
@author : Aymen Brahim Djelloul
Version : 1.0
Date : 29.08.2024
License : MIT


"""

# IMPORTS
import sys
import re
import subprocess
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


class Pi(PiCore):

    def __init__(self) -> None:
        super(Pi, self).__init__()


    def pi_model(self) -> str:
        """ This method will get the Raspberry Pi Model name string"""
        # NOT YET


    def serial_number(self) -> str:
        """ This method will get the Raspberry Pi internal serial number"""

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
        return int(self._get_query_data("Thread(s) per core:")) * int(self._get_query_data("CPU(s):"))\
              if logical else self._get_query_data("CPU(s):")



    def max_clock_speed(self, aliased: bool = True) -> float:
        """ This method will get the maximum cpu clock speed """

    def base_clock_speed(self, aliased: bool = True) -> float:
        """ This method will get the maximum cpu clock speed """

    def l1_cache_size(self, aliased: bool = True) -> int:
        """ This method will get the level 1 cache memory size on cpu """

    def l2_cache_size(self, aliased: bool = True) -> int:
        """ This method will get the level 2 cache memory size on cpu """

    def l3_cache_size(self, aliased: bool = True) -> int:
        """ This method will get the level 3 cache memory size on cpu """

    def is_overclock(self) -> bool:
        """ This method will get the cpu is overclocked or not """

    def voltage(self) -> float:
        """ This method will get the cpu regular voltage """




if __name__ == "__main__":
    sys.exit()
