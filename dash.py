#!/usr/bin/env python3
from os import geteuid
import lib.app as app
import subprocess


def is_xterm_installed():
    try:
        # Use the "which" command to check if "xterm" is in the PATH
        subprocess.check_output(["which", "xterm"])
        return True
    except subprocess.CalledProcessError:
        return False


def install_xterm():
    try:
        # Use apt to install xterm
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "xterm"])
        return True
    except subprocess.CalledProcessError:
        return False


def xterm_check():
    if not is_xterm_installed():
        if install_xterm():
            return True
        else:
            print("Failed to install xterm. Check your package manager and "
                  "permissions.")
            print("Packet capture will not work without xterm.")
            return False
    else:
        return True


def main():
    # root check
    if geteuid() != 0:
        print("You must be root to run this program.")
        exit(1)
    # check if xterm installed
    if not xterm_check():
        exit(1)
    prog = app.App()
    prog.mainloop()


if __name__ == '__main__':
    main()
