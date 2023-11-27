import sys
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Colors:
    OKGREEN: str = "\033[92m"
    FAIL: str = "\033[91m"
    ENDC: str = "\033[0m"


class Logger:
    def __call__(self, message: str, success: Optional[bool] = None) -> None:
        if success is True:
            print(f"[{Colors.OKGREEN}OK{Colors.ENDC}] {message}")
        elif success is False:
            print(f"[{Colors.FAIL}FALSE{Colors.ENDC}] {message}")
            sys.exit(1)
        else:
            print(message)
