#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author: sharly

import subprocess


class Shell:
    @staticmethod
    def invoke(cmd_command):
        """execute the shell"""
        output, errors = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        return o


if __name__ == '__main__':
    aa = Shell.invoke('appium -v').splitlines()[0].strip()
    print(aa)
