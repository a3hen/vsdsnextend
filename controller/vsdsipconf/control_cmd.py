#! /usr/bin/env python3
import os
import re
import sys
import textwrap
import time
import yaml

from .base import Base

class NetworkManager:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger
        self.network_manager_config = "/etc/NetworkManager/NetworkManager.conf"
        # self.netplan_file = '/etc/netplan/01-netcfg.yaml'
        
        self.netplan_dir = '/etc/netplan'
        self.netplan_file = None

    def set_network_manager_interfaces(self):
        try:
            # 修改 NetworkManager 配置文件
            config_content = ""
            with open(self.network_manager_config, "r") as f:
                config_content = f.read()

            config_content = config_content.replace(
                "managed=false", "managed=true")

            with open(self.network_manager_config, "w") as f:
                f.write(config_content)
            self.logger.log(f"修改 NetworkManager 配置文件 ({self.network_manager_config}) 方法完成")
            return True
        except Exception as e:
            print(f"ERROR - 重启 NetworkManager 服务失败：{e}")
            self.logger.log(f"ERROR - 重启 NetworkManager 服务失败：{e}")
            return False

    def restart_network_manager_service(self):
        try:
            # 重启 NetworkManager 服务
            self.base.com("systemctl restart NetworkManager.service")
            self.logger.log(f"执行命令：systemctl restart NetworkManager.service")
            return True
        except Exception as e:
            self.logger.log(f"ERROR - 重启 NetworkManager 服务失败：{e}")
            return False
        
    def find_main_config(self):
        # 获取目录下的所有文件
        files = os.listdir(self.netplan_dir)

        # 根据文件名排序
        files.sort()

        for file in files:
            if file.endswith('.yaml'):
                # 找到第一个以 .yaml 结尾的文件，即主要配置文件
                self.netplan_file = os.path.join(self.netplan_dir, file)
                
                # 备份原始文件
                self.backup_config()
                return self.netplan_file

    def backup_config(self):
        if self.netplan_file:
            if not os.path.join(self.netplan_file, '.vsds_bak'):
                command = f"cp {self.netplan_file} {self.netplan_file}.vsds_bak"
                result = self.base.com(command)
                self.logger.log(f"已备份{self.netplan_file}为{self.netplan_file}.vsds_bak")
            else:
                self.logger.log(f"备份文件 {self.netplan_file}.vsds_bak 已存在")

    def update_netplan_config(self):
        try:
            self.netplan_file = self.find_main_config()
            # 打开 netplan 配置文件进行修改
            with open(self.netplan_file, 'w') as file:
                file.write("network:\n")
                file.write("  version: 2\n")
                file.write("  renderer: NetworkManager\n")
            
            self.logger.log(f"修改 Netplan 配置文件 ({self.netplan_file}) 方法完成")
            return True
        except Exception as e:
            self.logger.log(f"ERROR - 修改 Netplan 配置失败：{e}")
            return False

    def apply_netplan_config(self):
        try:
            # 应用 Netplan 配置
            self.base.com("netplan apply")
            self.logger.log(f"执行命令：netplan apply\n")
            return True
        except Exception as e:
            self.logger.log(f"ERROR - 应用 Netplan 配置失败：{e}")
            return False


class Package:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger
        self.nmcli_versions = self.base.get_version_from_yaml("nmcli", self.install_from_yaml())
        
    def install_package(self):
        version = self.nmcli_versions
        command = f"apt install network-manager"
        if version is not None:
            command += f"={version}"
            self.logger.log(f"安装 nmcli 版本: {version}")
            print(f"安装 nmcli 版本: {version}")
        else:
            print(f"安装 nmcli 默认版本")
            self.logger.log(f"安装 nmcli 的默认版本")
        command += " -y"

        # print(f"command: {command} ")
        result = self.base.com(command)
        self.logger.log(f"执行 {command} 的结果: {result.stdout}")
        # print(f"结果: {result.stdout} ")
        if result.returncode != 0:
            self.logger.log(f"安装 nmcli 失败")
            print(f"安装 nmcli 失败")
            sys.exit()
        # print(f"安装 nmcli 成功")
        return result

    def install_from_yaml(self):
        yaml_filename = "vsdsipconf_config.yaml"
        yaml_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), yaml_filename)
        try:
            if not os.path.isfile(yaml_path):
                raise FileNotFoundError(f"未找到 {yaml_filename} 文件\n请检查配置文件是否在当前路径或者配置文件名称是否为 config.yaml")
            return yaml_path
        except FileNotFoundError as e:
            print(e)  
            sys.exit()
        
    def version_remain(self, software_name, version=None):
        result = self.base.com("")
        nmcli_match = None

        result = self.base.com(f"{software_name} --version")
        self.logger.log(f"{software_name} --version的执行结果: {result.stdout}")
        
        software_name = "network-manager"
        
        if "No such file" in result.stdout or "not found" in result.stdout:
            self.logger.log(f"安装 nmcli 失败")
            print(f"安装 nmcli 失败")
            sys.exit()
        elif version != None:
            print(f"安装 nmcli 成功")
            print(f"{software_name} 版本检查完成: {version}\n")
        else:
            nmcli_match = re.search(r'version (.+)', str(result.stdout))
            print(f"安装 nmcli 成功")
            print(f"{software_name} 版本检查完成: {nmcli_match.group(1)}\n")
            
    def check_versions(self):
        version = self.nmcli_versions
        # print(f"{software_name} version: {version}")
        self.version_remain('nmcli', version)
