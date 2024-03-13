#! /usr/bin/env python3
import os
from base import Base
from prettytable import PrettyTable


class System:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger

    # 停止无人值守升级
    def stop_unattended_upgrades(self):
        try:
            command = f"systemctl stop unattended-upgrades"
            result = self.base.com(command)
            self.logger.log(f"执行命令：{command}")
            return True
        except Exception as e:
            print(f"停止无人值守升级发生错误：{e}")
            self.logger.log(f"ERROR - 停止无人值守升级发生错误：{e}")  # debug
            return False

    # 禁用无人值守升级
    def disable_unattended_upgrades(self):
        try:
            command = f"systemctl disable unattended-upgrades"
            result = self.base.com(command)
            self.logger.log(f"执行命令：{command}")
            return True
        except Exception as e:
            print(f"禁用无人值守升级发生错误：{e}")
            self.logger.log(f"ERROR - 禁用无人值守升级发生错误：{e}")  # debug
            return False

    # 修改配置文件参数
    def modify_configuration_file_parameters(self):  # 权限问题？
        try:
            file_path = '/etc/apt/apt.conf.d/20auto-upgrades'
            self.logger.log(f"修改配置文件参数：{file_path}")
            new_content = ""

            # 检查文件是否存在             ///////////////
            if not os.path.exists(file_path):
                self.logger.log(f"ERROR - 文件 {file_path} 不存在")
                print(f"文件 {file_path} 不存在")
                return False
        
            # 打开文件并读取内容
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # 遍历文件的每一行，查找并替换目标参数
            for line in lines:
                if "APT::Periodic::Update-Package-Lists" in line:
                    new_content += 'APT::Periodic::Update-Package-Lists "0";\n'
                elif "APT::Periodic::Unattended-Upgrade" in line:
                    new_content += 'APT::Periodic::Unattended-Upgrade "0";\n'
                else:
                    new_content += line

            # 打开文件并写入修改后的内容
            with open(file_path, 'w') as file:
                file.write(new_content)

            return True
        except Exception as e:
            print(f"修改配置文件参数发生错误：{e}")
            self.logger.log(f"ERROR - 修改配置文件参数发生错误：{e}")  # debug
            return False

    # 检查是否禁用无人值守升级成功
    def check_unattended_upgrades(self):
        try:
            command = f"systemctl is-enabled unattended-upgrades"
            result = self.base.com(command)
            self.logger.log(f"执行命令：{command} 结果：{result.stdout.strip()}")
            self.logger.space()
            if "disabled" in result.stdout or "non-zero" in result.stdout:
                return True
            else:
                return False
        except Exception as e:
            print(f"检查是否禁用无人值守升级发生错误：{e}")
            self.logger.log(f"ERROR - 检查是否禁用无人值守升级发生错误：{e}\n")  # debug
            return False

    # 检查配置文件参数是否修改成功
    def check_configuration_file(self):
        try:
            command1 = f"apt-config dump APT::Periodic::Update-Package-Lists"
            command2 = f"apt-config dump APT::Periodic::Unattended-Upgrade"
            result_Update_Package_Lists = self.base.com(command1)
            self.logger.log(f"执行结果：{result_Update_Package_Lists.stdout.strip()}")
            result_Unattended_Upgrade = self.base.com(command2)
            self.logger.log(f"执行结果：{result_Unattended_Upgrade.stdout.strip()}")
            if "0" not in result_Update_Package_Lists.stdout and "0" not in result_Unattended_Upgrade.stdout:
                return False
            else:
                return True
        except Exception as e:
            print(f"检查配置文件参数是否修改成功发生错误：{e}")
            self.logger.log(f"ERROR - 检查配置文件参数是否修改成功发生错误：{e}")  # debug
            return False
    # 显示系统状态

    def display_system_status(self):
        try:
            # 服务名称
            services = ["unattended-upgrades", "linstor-controller",
                        "linstor-satellite", "rtslib-fb-targetctl", "pacemaker", "corosync"]

            # 创建一个 PrettyTable 来展示状态
            status_table = PrettyTable()
            status_table.field_names = ["Service", "Active", "Enabled"]

            for service in services:
                active_status = self.get_service_active_status(service)
                enabled_status = self.get_service_enabled_status(service)

                # 添加服务状态到表格
                status_table.add_row([service, active_status, enabled_status])

            # 打印系统状态
            print("System Status:")
            print(status_table)
            self.logger.log(f"System Status displayed\n{status_table}")

        except Exception as e:
            print(f"显示系统状态发生错误：{e}")
            self.logger.log(f"ERROR - 显示系统状态发生错误：{e}")

    # 获取服务的活动状态
    def get_service_active_status(self, service_name):
        try:
            command = f"systemctl is-active {service_name}"
            result = self.base.com(command).stdout.strip()
            self.logger.log(f"执行命令：{command} 结果：{result}")
            return result.strip()  # 去掉首尾空白字符
        except Exception as e:
            return f"ERROR - {str(e)}"

    # 获取服务的开机自启状态
    def get_service_enabled_status(self, service_name):
        try:
            command = f"systemctl is-enabled {service_name}"
            result = self.base.com(command).stdout.strip()
            self.logger.log(f"执行命令：{command} 结果：{result}")
            return result.strip()  # 去掉首尾空白字符
        except Exception as e:
            return f"ERROR - {str(e)}"
