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
                
                else:
                
                    # Clear memory
                    del line, pattern

        # Second method: Using 'cat /proc/cpuinfo'
        if self.cpuinfo_data:
            for line in self.cpuinfo_data.splitlines():
                if line.startswith(pattern):
                    return line.split(':', 1)[1].strip()
                
                else:
                    
                    # Clear memory
                    del line, pattern

       

        # Other-wise return None
        else:
            return None


class Pi(PiCore):

    def __init__(self) -> None:
        super(Pi, self).__init__()


    def pi_model(self) -> str:
        """ This method will get the Raspberry Pi Model name string"""
        # NOT YET
        return ""


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
        """ This method will get the cpu is overclocked or not """

    def voltage(self) -> float:
        """ This method will get the cpu regular voltage """




if __name__ == "__main__":
    sys.exit()
