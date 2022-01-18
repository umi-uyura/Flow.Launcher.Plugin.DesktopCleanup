# -*- coding: utf-8 -*-

import copy
import os
from ctypes import *
from typing import List

from flowlauncher import FlowLauncher
from flowlauncher import FlowLauncherAPI as API

import plugin.fileclean as cleaner
from plugin.extensions import _l
from plugin.templates import *


class Main(FlowLauncher):
    user32 = windll.user32
    messages_queue = []

    def sendNormalMess(self, title: str, subtitle: str):
        message = copy.deepcopy(RESULT_TEMPLATE)
        message["Title"] = title
        message["SubTitle"] = subtitle

        self.messages_queue.append(message)

    def sendActionMess(self, title: str, subtitle: str, method: str, value: List):
        # information
        message = copy.deepcopy(RESULT_TEMPLATE)
        message["Title"] = title
        message["SubTitle"] = subtitle

        # action
        action = copy.deepcopy(ACTION_TEMPLATE)
        action["JsonRPCAction"]["method"] = method
        action["JsonRPCAction"]["parameters"] = value
        message.update(action)

        self.messages_queue.append(message)

    def query(self, param: str) -> List[dict]:
        self.messages_queue.clear()

        q = param.strip()

        if len(q) == 0:
            self.sendActionMess(
                "clean",
                _l("DESCRIPTION_COMMAND_CLEAN"),
                "cleanup",
                [["remove", _l("DESCRIPTION_COMMAND_CLEAN")]]
            )
            self.sendActionMess(
                "trash",
                _l("DESCRIPTION_COMMAND_TRASH"),
                "cleanup",
                [["trash", _l("DESCRIPTION_COMMAND_TRASH")]]
            )
        elif q == "clean":
            self.sendActionMess(
                "clean",
                _l("DESCRIPTION_COMMAND_CLEAN"),
                "cleanup",
                [["remove", _l("DESCRIPTION_COMMAND_CLEAN")]]
            )
        elif q == "trash":
            self.sendActionMess(
                "trash",
                _l("DESCRIPTION_COMMAND_TRASH"),
                "cleanup",
                [["trash", _l("DESCRIPTION_COMMAND_TRASH")]]
            )

        return self.messages_queue

    def cleanup(self, value):
        operation = value[0]
        msg = value[1]

        answer = self.user32.MessageBoxW(
            0,
            msg,
            "Desktop Cleanup",
            0x00000001 | 0x00000030)
        
        if answer == 2:
            return

        desktop_dir = os.path.expanduser('~\Desktop')
        public_path = os.path.join(os.path.expandvars("%public%"), "Desktop")
        results = (0, 0, [])

        if operation == "remove":
            results = cleaner.remove(desktop_dir)
            results = cleaner.remove(public_path, results)
        elif operation == "trash":
            results = cleaner.trash(desktop_dir)
            results = cleaner.trash(public_path, results)

        msg1 = _l("MESSAGE_CLEAN_PROCESSED").format(results[0], results[1])
        msg2 = _l("MESSAGE_CLEAN_ERROR_OCCURRED").format(len(results[2]))

        if len(results[2]) == 0:
            API.show_msg(
                "Desktop Cleanup",
                msg1,
                "assets/icon.png"
            )
        else:
            API.show_msg(
                "Desktop Cleanup",
                msg1 + os.linesep + msg2,
                "assets/icon.png"
            )
