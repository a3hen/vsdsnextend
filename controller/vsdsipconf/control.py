#! /usr/bin/env python3
from .control_cmd import NetworkManager, Package

def Singleton(cls):
    instance = {}

    def _singleton_wrapper(*args, **kargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kargs)
        return instance[cls]

    return _singleton_wrapper

def display_version():
    print("version: v1.0.2")

@Singleton
class Control:
    def __init__(self, logger):
        self.network_manager = NetworkManager(logger)
        self.package = Package(logger)
        self.print_ = []
            
    # nmcli安装
    def nmcli_(self):
        self.package.install_package()
        self.package.check_versions()

    # 配置 Network Manager
    def setup_network_manager(self):
        if not self.network_manager.set_network_manager_interfaces():
            print(f"修改NetworkManager.conf失败")
        if not self.network_manager.restart_network_manager_service():
            print(f"重启NetworkManager服务失败")
        if not self.network_manager.update_netplan_config():
            print(f"修改01-netcfg.yaml失败")
        if not self.network_manager.apply_netplan_config():
            print(f"应用 Netplan 配置失败")
        else:
            print("配置网络管理成功")

        print("done")
    
    # 最后进行一次重启 network_manager
    def restart_network_manager(self):
        if not self.network_manager.restart_network_manager_service():
            print(f"重启NetworkManager服务失败")

    def all_control(self):
        self.nmcli_()
        self.setup_network_manager()
        self.restart_network_manager()