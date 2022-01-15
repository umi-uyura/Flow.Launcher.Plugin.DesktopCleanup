# -*- coding: utf-8 -*-

import os
import sys

from swinlnk.swinlnk import SWinLnk
from win32com.shell import shell, shellcon

import plugin.fileclean as cleaner

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

swl = SWinLnk()

def generate_test_files():
    desktop_path = os.path.expanduser('~\Desktop')
    public_path = os.path.expandvars("%public%")
    system_path = os.path.expandvars("%windir%")

    notepad_src_path = os.path.join(system_path, "System32", "notepad.exe")
    notepad_dst_path = os.path.join(desktop_path, "notepad.lnk")
    swl.create_lnk(notepad_src_path, notepad_dst_path)

    calc_src_path = os.path.join(system_path, "System32", "calc.exe")
    calc_dst_path = os.path.join(desktop_path, "calc.lnk")
    swl.create_lnk(calc_src_path, calc_dst_path)

    cmd_src_path = os.path.join(system_path, "System32", "cmd.exe")
    cmd_dst_path = os.path.join(desktop_path, "cmd.lnk")
    swl.create_lnk(cmd_src_path, cmd_dst_path)

    os.mkdir(os.path.join(desktop_path, "dc_test"))

    explorer_src_path = os.path.join(system_path, "explorer.exe")
    explorer_dst_path = os.path.join(desktop_path, "dc_test", "explorer.lnk")
    swl.create_lnk(explorer_src_path, explorer_dst_path)

    regedit_src_path = os.path.join(system_path, "regedit.exe")
    regedit_dst_path = os.path.join(desktop_path, "dc_test", "regedit.lnk")
    swl.create_lnk(regedit_src_path, regedit_dst_path)

    magnify_src_path = os.path.join(system_path, "System32", "Magnify.exe")
    magnify_tmp_path = os.path.join(desktop_path, "Magnify.lnk")
    magnify_dst_path = os.path.join(public_path, "Desktop", "Magnify.lnk")
    swl.create_lnk(magnify_src_path, magnify_tmp_path)
    shell.SHFileOperation((0, shellcon.FO_MOVE, magnify_tmp_path, magnify_dst_path))


if __name__ == "__main__":
    gen_only = sys.argv[1] if len(sys.argv) > 1 else ""
    if gen_only == "genonly":
        generate_test_files()
        sys.exit()

    print("test start")

    desktop_dir = os.path.expanduser('~\Desktop')
    public_path = os.path.expandvars("%public%")
    public_desktop_dir = os.path.join(public_path, "Desktop")

    #
    # Remove file/directory test
    #

    generate_test_files()

    before_outcome = len(os.listdir(desktop_dir))
    outcome = cleaner.remove(desktop_dir)
    print(f"Processing = {outcome}, Desktop = {before_outcome} -> {len(os.listdir(desktop_dir))}")

    public_before_counts = len(os.listdir(public_desktop_dir))
    outcome = cleaner.remove(public_desktop_dir, outcome)
    print(f"Processing = {outcome}, Public Desktop = {public_before_counts} -> {len(os.listdir(public_desktop_dir))}")

    if len(outcome[2]) > 0:
        print(f"    error = {os.linesep.join([str(e) for e in outcome[2]])}")

    #
    # Move to trash test
    #

    if shell.SHQueryRecycleBin()[1] > 0:
        shell.SHEmptyRecycleBin(None, None, 1)

    generate_test_files()

    before_outcome = len(os.listdir(desktop_dir))
    outcome = cleaner.trash(desktop_dir)
    print(f"Processing = {outcome}, Recycle Bin = {before_outcome} -> {shell.SHQueryRecycleBin()[1]}")

    public_before_counts = len(os.listdir(public_desktop_dir))
    outcome = cleaner.trash(public_desktop_dir, outcome)
    print(f"Processing = {outcome}, Public Recycle Bin = {public_before_counts} -> {shell.SHQueryRecycleBin()[1]}")

    if len(outcome[2]) > 0:
        print(f"    error = {os.linesep.join([str(e) for e in outcome[2]])}")
