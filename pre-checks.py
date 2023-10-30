#!/usr/bin/env python3

import run as run
from os import geteuid
import subprocess


def check_tkinter():
    try:
        import tkinter
        return True
    except ImportError:
        return False


def install_tkinter():
    try:
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "python3-tk"])
        return True
    except subprocess.CalledProcessError:
        return False


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


def check_root():
    if geteuid() != 0:
        print("You must be root to run this program.")
        exit(1)


def run_checks():
    check_root()
    if not check_tkinter():
        if install_tkinter():
            print("Tkinter installed.")
        else:
            print("Failed to install tkinter. Check your package manager and "
                  "permissions.")
            exit(1)
    if not xterm_check():
        exit(1)
    print("All checks passed.")
    run.run_app()


if __name__ == '__main__':
    run_checks()
