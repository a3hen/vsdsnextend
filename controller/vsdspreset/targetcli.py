#! /usr/bin/env python3
from base import Base


class TargetCLIConfig:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger
    
    def configure_targetcli(self, buffer):
        try:
            # 配置 targetcli
            command = f"targetcli set global {buffer}"
            self.base.com(command)
            self.logger.log(f"执行命令：{command}")
            return True
        except Exception as e:
            self.logger.log(f"ERROR - 配置targetcli失败: {e}")
            return False

    def check_targetcli_configuration(self, buffer):
        try:
            # 检查 targetcli 配置
            command = f"targetcli get global {buffer}"

            if buffer == "auto_add_default_portal" or buffer == "auto_add_mapped_luns":
                if "false" not in self.base.com(command).stdout:
                    self.logger.log(f"ERROR - auto_add_default_portal配置失败：{command}")
                    return False
                else:
                    self.logger.log(f"执行命令：{command} 结果：{self.base.com(command).stdout.strip()}")
                    print(f"检查 {buffer} 通过")
                    return True
            elif buffer == "auto_enable_tpgt":
                if "true" not in self.base.com(command).stdout:
                    self.logger.log(f"ERROR - auto_enable_tpgt配置失败：{command}")
                    return False
                else:
                    self.logger.log(f"执行命令：{command} 结果：{self.base.com(command).stdout.strip()}")
                    print(f"检查 {buffer} 通过")
                    return True
            buffer = None
        except Exception as e:
            self.logger.log(f"ERROR - 检查 targetcli 配置失败: {e}")
            return False
