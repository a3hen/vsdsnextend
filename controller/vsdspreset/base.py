
#! /usr/bin/env python3

import subprocess


class Base:
    def __init__(self, logger):
        self.logger = logger

    def com(self, command):
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
            return result
        except subprocess.CalledProcessError as e:
            self.logger.log(f"命令 {command} 执行失败 {e}")
            return f"命令执行失败: {str(e)}"
