"""
@author : Aymen Brahim Djelloul
Date : 29.08.2024
License : MIT

"""

# IMPORTS
import sys


class NotSUpportedPlatform(BaseException):

    def __init__(self, platform: str, supported: str) -> None:
        self.platform = platform
        self.supported_platforms = supported

    def __str__(self) -> str:
        return f""
    

class RunningOnVirtualMachine(BaseException):

    def __str__(self) -> str:
        return ""


if __name__ == "__main__":
    sys.exit()
    