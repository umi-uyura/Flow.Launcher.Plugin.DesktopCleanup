# -*- coding: utf-8 -*-

import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from send2trash import send2trash

class FILECLEAN_TARGET_TYPE(Enum):
    FILE = 1
    DIRECTORY = 2
    UNKNOWN = 99

@dataclass(frozen=True)
class FileCleanErrorInfo:
    type: FILECLEAN_TARGET_TYPE
    name: str
    err: str
    code: int

    def __str__(self) -> str:
        return f"type={self.type.name}, name='{self.name}', err={self.err} ({self.code})"

def remove(path, outcome=(0, 0, [])):
    p = Path(path)

    for f in p.glob("*"):
        err = None

        isfile = f.is_file()
        isdir = f.is_dir()

        if isfile and "desktop.ini" == f.name:
            continue

        if isdir:
            try:
                shutil.rmtree(f)
            except OSError as e:
                err = FileCleanErrorInfo(FILECLEAN_TARGET_TYPE.DIRECTORY, e.filename, e.strerror, e.winerror)
        elif isfile:
            try:
                f.unlink()
            except OSError as e:
                err = FileCleanErrorInfo(FILECLEAN_TARGET_TYPE.FILE, e.filename, e.strerror, e.winerror)
        else:
            err = FileCleanErrorInfo(FILECLEAN_TARGET_TYPE.UNKNOWN, f.name, str(f.stat()), 0)

        count_file = outcome[0]
        count_dir = outcome[1]
        error_list = outcome[2] if err is None else outcome[2] + [err]

        if isfile and err is None:
            count_file = outcome[0] + 1
        elif isdir and err is None:
            count_dir = outcome[1] + 1

        outcome = (count_file, count_dir, error_list)

    return outcome

def trash(path, outcome=(0, 0, [])):
    p = Path(path)

    for f in p.glob("*"):
        err = None

        isfile = f.is_file()
        isdir = f.is_dir()
        fname = f.name

        if isfile and "desktop.ini" == f.name:
            continue

        if isfile or isdir:
            try:
                send2trash(str(f))
            except OSError as e:
                type = FILECLEAN_TARGET_TYPE.UNKNOWN
                if isfile:
                    type = FILECLEAN_TARGET_TYPE.FILE
                if isdir:
                    type = FILECLEAN_TARGET_TYPE.DIRECTORY
                err = FileCleanErrorInfo(type, e.filename, e.strerror, e.winerror)
        else:
            err = [FileCleanErrorInfo(FILECLEAN_TARGET_TYPE.UNKNOWN, fname, str(f.stat()), 0)]

        count_file = outcome[0]
        count_dir = outcome[1]
        error_list = outcome[2] if err is None else outcome[2] + [err]

        if isfile and err is None:
            count_file = outcome[0] + 1
        if isdir and err is None:
            count_dir = outcome[1] + 1

        outcome = (count_file, count_dir, error_list)

    return outcome
