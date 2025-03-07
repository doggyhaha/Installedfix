import os
import sys
import re
import winreg
import ctypes
import time
from typing import List
from dataclasses import dataclass


UNINSTALL_PATH_X86 = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
UNINSTALL_PATH_X64 = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"

HKEYS_CHECK = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]


@dataclass
class InstalledProgram:
    display_name: str
    uninstall_string: str
    uninstall_path: str
    context: int  # winreg.HKEY_LOCAL_MACHINE or winreg.HKEY_CURRENT_USER
    key: str


def ensure_privileges():
    admin = ctypes.windll.shell32.IsUserAnAdmin()
    if not admin:
        print("You need to run this script as an administrator.")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()


ensure_privileges()


def filter_programs(
    installed_programs: List[InstalledProgram],
) -> List[InstalledProgram]:
    # receives {display_name: uninstall_string}
    # returns {display_name: uninstall_string} with only unexisting uninstallers
    pattern = re.compile(
        r'[A-Za-z]:\\(?:[^<>:"\/\\|?*\r\n]+\\)*[^<>:"\/\\|?*\r\n]+\.\w+'
    )  # should match a path to a file with an extension
    invalid_unins = []
    for program in installed_programs:
        match = pattern.search(program.uninstall_string)
        if match:
            if not os.path.exists(path := match.group()):
                if "bluestacks" in program.display_name.lower():
                    print(program.uninstall_string)
                    print(match.group())
                invalid_unins.append(
                    InstalledProgram(
                        program.display_name,
                        program.uninstall_string,
                        path,
                        program.context,
                        program.key,
                    )
                )
    return invalid_unins


def get_invalid_uninstallers() -> List[InstalledProgram]:
    programs = []
    for path in [UNINSTALL_PATH_X86, UNINSTALL_PATH_X64]:
        for hkey in HKEYS_CHECK:
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_READ) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                display_name = winreg.QueryValueEx(
                                    subkey, "DisplayName"
                                )[0]
                                uninstall_string = winreg.QueryValueEx(
                                    subkey, "UninstallString"
                                )[0]
                                full_key = f"{path}\\{subkey_name}"
                                programs.append(
                                    InstalledProgram(
                                        display_name,
                                        uninstall_string,
                                        "",
                                        hkey,
                                        full_key,
                                    )
                                )
                            except FileNotFoundError:
                                pass
                    except OSError:
                        pass
    return filter_programs(programs)


def remove_entries(programs: List[InstalledProgram]):
    t = time.strftime("%Y-%m-%d-%H-%M-%S")
    with open(f"removed_{t}.txt", "w", encoding="utf-8") as f:
        for program in programs:
            print(f"Removing {program.display_name}...")
            try:
                winreg.DeleteKey(program.context, program.key)
                print("Removed.")
                f.write(f"{program.display_name}\n")
            except OSError as e:
                print(f"Failed to remove {program.display_name}: {e}")



def main():
    print(
        "First of all, make a backup of your registry by running regedit and clicking on File -> Export -> All."
    )
    print("This script will remove invalid uninstallers from the registry.")
    backed_up = False
    while not backed_up:
        print("Did you backup? (y/N)")
        if input().lower() == "y":
            backed_up = True
        else:
            print("Please backup before proceeding.")

    invalid_uninstallers = get_invalid_uninstallers()
    to_remove = []
    if invalid_uninstallers:
        print("The following uninstallers are invalid:")
        for i, program in enumerate(invalid_uninstallers):
            print(f"{i + 1}. {program.display_name}")
            rem = input("Remove? (y/N): ")
            if rem.lower() == "y":
                to_remove.append(program)
    else:
        print("No invalid uninstallers found.")

    if to_remove:
        remove_entries(to_remove)


if __name__ == "__main__":
    main()
