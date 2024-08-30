"""
@author : Aymen Brahim DJelloul
Version : 1.0
Date : 29.08.2024
License : MIT


    // The module 'utils.py' is a pretty straight-forward module provides necessarly functions
    for PiCore software


"""

# IMPORTS
import re
import sys
import subprocess
from const import *
from math import ceil



def get_system_id() -> str:
    """ This method will get Operating system id name like 'debian' or 'Ubuntu' """
    try:
        # Open the 'os-release' file
        with open(OS_RELEASE) as f:
            # Read data
            _output = f.read()

        # Search for the ID line and extract the value
        match = re.search(r'^ID=(\w+)', _output, re.MULTILINE)
        if match:
            # Return the ID value
            return match.group(1)
        else:
            return None

    except FileNotFoundError:
        return None
    


def is_virtual_machine() -> bool:    
    """
    Check if the Linux-based system is running inside a virtual machine.
    Returns:
        bool: True if the system is a VM, False otherwise.
    """
        
    try:

        # Check for specific virtual machine files in /sys/class/dmi/id/
        try:
            dmi_files = ['/sys/class/dmi/id/product_name', '/sys/class/dmi/id/sys_vendor']
            for file in dmi_files:
                try:
                    with open(file, 'r') as f:
                        content = f.read()
                        if any(vm_indicator in content for vm_indicator in ['VMware', 'VirtualBox', 'KVM', 'QEMU']):
                            return True
                except FileNotFoundError:
                    continue
        except IOError:
            pass

        # Check for presence of virtualization module
        try:
            modules = subprocess.check_output(['lsmod'], text=True)
            if any(vm_module in modules for vm_module in ['kvm', 'vboxdrv', 'vmwgfx']):
                return True
        except subprocess.CalledProcessError:
            pass


        # Check /proc/cpuinfo for hypervisor presence
        try:
            cpuinfo = subprocess.check_output(['cat', '/proc/cpuinfo'], text=True)
            if 'hypervisor' in cpuinfo.lower():
                return True
        except subprocess.CalledProcessError:
            pass

        # If no VM indicators found
        return False

    except Exception as e:
        # Catch any other exceptions and assume it's not a VM
        print(f"An unexpected error occurred: {e}")
        return False


def mhz_to_ghz(value: float) -> float:
    """ This method will conveert Mhz to Ghz value"""
    return ceil(value / 1000.0)


def mb_to_kb(value: int) -> float:
    """ This method will convert megabytes to kilobytes """
    return value * 1024

def kb_to_bytes(value: int) -> float:
    """ This method will convert kilobytes to bytes """
    return value // 1024

def mb_to_bytes(value: int) -> float:
    """ This method will convert megabytes to bytes"""
    return value * 2048

if __name__ == "__main__":
    sys.exit()
