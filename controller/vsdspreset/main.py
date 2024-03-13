#! /usr/bin/env python3

import argparse
import sys
from system import System
from log_record import Logger
from targetcli import TargetCLIConfig
from versds import VersaSDS

# 禁用系统自动升级
def disable_system_upgrades(system):
    if system.stop_unattended_upgrades() and system.disable_unattended_upgrades():
        if not system.check_unattended_upgrades():
            print("禁用无人值守升级失败，程序将继续执行")
        else:
            print("禁用无人值守升级成功")
    else: 
        print("禁用无人值守升级失败，程序将继续执行")

    if system.modify_configuration_file_parameters():
        if not system.check_configuration_file():
            print("配置文件参数修改失败，程序将继续执行后面内容")
        else:
            print("配置文件参数修改成功")
    else:
        print("配置文件参数修改失败，程序将继续执行后面内容")

    print("done")

# 禁用 VersaSDS 服务开机自启
def disable_VersaSDS_service_startup(versds):
    versds.implementation_methods()
    print("done")

# 配置 Network Manager
# def setup_network_manager(network_manager):
#     if not network_manager.set_network_manager_interfaces():
#         print(f"修改NetworkManager.conf失败")
#     if not network_manager.restart_network_manager_service():
#         print(f"重启NetworkManager服务失败")
#     if not network_manager.update_netplan_config():
#         print(f"修改01-netcfg.yaml失败")
#     if not network_manager.apply_netplan_config():
#         print(f"应用 Netplan 配置失败")
#     else:
#         print("配置网络管理成功")

#     print("done")

# 初始化 targetcli 配置


def initialize_targetcli_configuration(targetcli):
    config_items = [
        ("auto_add_default_portal=false", "auto_add_default_portal"),
        ("auto_add_mapped_luns=false", "auto_add_mapped_luns"),
        ("auto_enable_tpgt=true", "auto_enable_tpgt")
    ]
    note = "初始化 targetcli 配置失败"

    for config_value, config_name in config_items:
        if not targetcli.configure_targetcli(config_value):
            print(f"{config_name}: {note}")
        elif not targetcli.check_targetcli_configuration(config_name):
            print(f"{config_name}: {note}")

    print("done")

def display_system_status(system):
    system.display_system_status()

def display_version():
    print("version: v1.0.1")

def main():
    parser = argparse.ArgumentParser(description='vsdspreset')
    parser.add_argument('-d', '--display', action='store_true', 
                        help=argparse.SUPPRESS)
    parser.add_argument('-u', '--upgrade', action='store_true',
                        help='Disable system upgrades')
    parser.add_argument('-s', '--service', action='store_true',
                        help='Disable VersaSDS service startup')
    # parser.add_argument('-n', '--network', action='store_true',
                        # help='Setup Network Manager')
    parser.add_argument('-i', '--initialize', action='store_true',
                        help='Initialize TargetCLI Configuration')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Show version information')
    # parser.add_argument('--skip', action='store_true',
    #                     help='Skip Setup Network Manager')
    args = parser.parse_args()

    if args.version:
        display_version()
        sys.exit()

    logger = Logger("vsdspreset")
    system = System(logger)
    versds = VersaSDS(logger)
    # network_manager = NetworkManager(logger)
    targetcli = TargetCLIConfig(logger)

    if args.upgrade:
        disable_system_upgrades(system)
    elif args.service:
        disable_VersaSDS_service_startup(versds)
    # elif args.network:
    #     setup_network_manager(network_manager)
    elif args.initialize:
        initialize_targetcli_configuration(targetcli)
    elif args.display:
        display_system_status(system)
    else:
        disable_system_upgrades(system)
        disable_VersaSDS_service_startup(versds)
        # setup_network_manager(network_manager)
        initialize_targetcli_configuration(targetcli)

if __name__ == '__main__':
    main()

# if __name__ == '__main__':
#     # 使用 sudo 来运行脚本以获取足够的权限
#     os.system('sudo python your_script.py')
