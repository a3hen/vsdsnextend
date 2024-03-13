import sys
import os
import yaml
import subprocess
from controller import (vsdsipconf,
                        vsdsiptool,
                        vsdssshfree,
                        vsdsinstaller_k,
                        vsdsinstaller_u,
                        vsdspreset,
                        vsdsadm,
                        vsdscoroconf,
                        vsdshaconf,
                        csmpreinstaller)


def check_root():
    if os.geteuid() != 0:
        print("此脚本需要 root 权限运行。请以 root 用户执行此操作。")
        sys.exit(1)


class Control:
    def __init__(self):
        self.config_list = self.read_yaml()
        self.main()

    def main(self):
        print("节点拓展程序")
        print("* * * * * * * * * * * * * * * *")
        print("  请选择要执行的操作(1~12)，按其他键退出程序:")
        print("  1: * 顺序执行配置流程")
        print("  2: 安装和配置network manager")
        print("  3: 配置网络")
        print("  4: 实现ssh绵密")
        print("  5: 安装DRBD和LINSTOR")
        print("  6: 安装Pacemaker、Corosync、crmsh等")
        print("  7: VersaSDS预配置")
        print("  8: 配置LVM和LINSTOR集群")
        print("  9: 配置Corosync")
        print("  10: 配置高可用环境")
        print("  11: 安装Docker和Kubeadm等软件")
        print("  12: 退出")
        print("* * * * * * * * * * * * * * * *")
        user_input = input("请输入操作: ").lower()
        if user_input == '1':
            self.replacement_kernel_check()
            self.vsdsipconf()
            self.vsdsiptool()
            self.vsdssshfree()
            self.vsdsinstaller_k()
            self.vsdsinstaller_u()
            self.vsdspreset()
            self.vsdsadm()
            self.vsdscoroconf()
            self.vsdshaconf()
            self.csmpreinstaller()
        elif user_input == '2':
            self.vsdsipconf()
        elif user_input == '3':
            self.vsdsiptool()
        elif user_input == '4':
            self.vsdssshfree()
        elif user_input == '5':
            self.vsdsinstaller_k()
        elif user_input == '6':
            self.vsdsinstaller_u()
        elif user_input == '7':
            self.vsdspreset()
        elif user_input == "8":
            self.vsdsadm()
        elif user_input == '9':
            self.vsdscoroconf()
        elif user_input == '10':
            self.vsdshaconf()
        elif user_input == '11':
            self.csmpreinstaller()
        elif user_input == '12':
            sys.exit()
        else:
            print("退出程序")
            sys.exit()

    def read_yaml(self):
        file_path = './config.yaml'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                return data
        except FileNotFoundError:
            print(f"配置文件 {file_path} 未找到。")
            return None
        except yaml.YAMLError as exc:
            print(f"解析 YAML 文件时出错: {exc}")
            return None

    def replacement_kernel_check(self):
        user_input = input("是否按照要求替换好内核 (y/n)，按其他键退出程序").lower()
        if user_input == 'y':
            print("已替换好内核，即将安装软件")
        elif user_input.lower() == 'n':
            print("请先替换内核，再安装软件")
        else:
            print("请先替换内核，再安装软件")
            sys.exit()

    def vsdsipconf(self):
        print("安装网络配置工具，若已安装可跳过")
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过安装网络配置").lower()
        if user_input == 'y':
            print("执行'y'的操作")
            obj = vsdsipconf.control.Control()
            obj.all_control()
        elif user_input.lower() == 'n':
            print("执行'n'的操作")
            print("请先填写配置文件")
            print("退出程序")
            sys.exit()
        else:
            print("退出网络配置工具安装")
            print("程序继续执行")

    def vsdsiptool(self):
        print("ip 配置，若已配置 ip 可跳过")
        user_input = input("是否跳过 ip 配置 (y/n)，按其他键跳过 ip 配置").lower()
        if user_input == 'y':
            print("退出 ip 配置")
            print("程序继续执行")
        elif user_input.lower() == 'n':
            print("* * * * * * * * * * * * * * * *")
            print("  请选择要执行的操作(1~3):")
            print("  1: 配置Bonding网络")
            print("  2: 配置普通网络")
            print("  3: 结束")
            print("* * * * * * * * * * * * * * * *")
            while True:
                choose_input = input("请选择要执行的操作: ").lower()
                if choose_input == '1':
                    print("请输入 bonding 网卡名、ip、网络接口1（子网卡1）、网络接口2（子网卡2） 和 bonding 模式")
                    bond_name = input("bonding 网卡名: ")
                    ip = input("ip: ")
                    interface_1 = input("网络接口1（子网卡1）: ")
                    interface_2 = input("网络接口2（子网卡2）: ")
                    bond_mode = input("bonding 模式: ")
                    # 执行命令
                    break
                elif choose_input == '2':
                    print("请输入 ip 和 网络接口（网卡）")
                    ip = input("ip: ")
                    interface = input("网络接口（网卡）: ")
                    # 执行命令
                    break
                elif choose_input == '3':
                    break
                else:
                    print("无效的选择，请重新输入")
        else:
            print("退出 ip 配置")
            print("程序继续执行")

    def vsdssshfree(self):
        print("进行 ssh 免密配置，如已配置可跳过")
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过 ssh 免密配置").lower()
        if user_input == "y":
            pass
        elif user_input == "n":
            print("请先填写配置文件")
            print("退出程序")
        else:
            print("跳过 ssh 免密配置")
            print("程序继续执行")

    # 执行vsdsinstaller-k -i，安装 DRBD/LINSTOR
    def vsdsinstaller_k(self):
        print("安装DRBD/LINSTOR，若已安装可跳过")
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过 DRBD/LINSTOR 安装").lower()
        if user_input == "y":
            pass
        elif user_input == "n":
            print("请先填写配置文件")
            print("退出程序")
            sys.exit()
        else:
            print("跳过 DRBD/LINSTOR 安装")
            print("程序继续执行")

    # 执行vsdsinstaller-u，安装 VersaSDS - Pacemaker/Corosync/crmsh  + targetcli
    def vsdsinstaller_u(self):
        print("安装高可用软件，若已安装可跳过")
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过高可用软件安装").lower()
        if user_input == "y":
            pass
        elif user_input == "n":
            print("请先填写配置文件")
            print("退出程序")
            sys.exit()
        else:
            print("跳过高可用软件安装")
            print("程序继续执行")

    # 执行vsdspreset，VersaSDS 预配置
    def vsdspreset(self):
        print("VersaSDS 预配置，若已配置可跳过")
        user_input = input("是否进行 VersaSDS 预配置 (y/n)，按其他键跳过 VersaSDS 预配置").lower()
        if user_input == "y":
            pass
        elif user_input == "n":
            print("退出程序")
            sys.exit()
        else:
            print("跳过 VersaSDS 预配置")
            print("程序继续执行")

    # 执行vsdsadm，配置 LVM 和 LINSTOR 集群
    def vsdsadm(self):
        # 检查config_list中的特定值是否为None
        if self.config_list['controller_ip'] is None or self.config_list['passphrase'] is None or self.config_list[
            'local_node_name'] is None or self.config_list[
            'local_node_ip'] is None:
            print("警告：'controller_ip'、'passphrase'、'local_node_name'或'local_node_ip'未配置，请检查config.yaml文件的填写。")
            return
        print("配置 LVM 和 LINSTOR 集群，如已配置可以跳过")
        user_input = input("是否配置 LVM 和 LINSTOR 集群 (y/n)，按其他键跳过配置 LVM 和 LINSTOR 集群").lower()
        if user_input == "y":
            pass
            # 配置linstor-client.conf
            vsdsadm.main.create_or_update_linstor_conf(controller_ip=self.config_list['controller_ip'])
            # 配置linstor.toml
            vsdsadm.main.append_fixed_content_to_file(password=self.config_list['passphrase'])
            # 创建新节点
            vsdsadm.main.create_node(node_name=self.config_list[
            'local_node_name'], node_ip=self.config_list[
            'local_node_ip'])
            # 调整 linstordb 副本
            vsdsadm.main.adjusting_linstordb()
            # 调整 PVC 副本
            vsdsadm.main.adjusting_pvc()
            # 开启satellite和controller
            vsdsadm.main.start_satellite()
            vsdsadm.main.start_controller()
        elif user_input == "n":
            print("退出程序")
            sys.exit()
        else:
            print("跳过配置 LVM 和 LINSTOR 集群")
            print("程序继续执行")

    def vsdscoroconf(self):
        print("配置 Corosync，如已配置可以跳过")
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过 Corosync 配置 ").lower()
        if user_input == "y":
            pass
        elif user_input == "n":
            print("请先填写配置文件")
            print("退出程序")
            sys.exit()
        else:
            print("跳过 Corosync 配置")
            print("程序继续执行")

    def vsdshaconf(self):
        print("配置高可用，如已配置可以跳过")
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过高可用配置 ").lower()
        if user_input == "y":
            pass
        elif user_input == "n":
            print("请先填写配置文件")
            print("退出程序")
            sys.exit()
        else:
            print("跳过高可用配置")
            print("程序继续执行")

    def csmpreinstaller(self):
        print("安装 docker & kubeadm 等软件")
        user_input = input("是否执行安装 (y/n)，按其他键跳过安装 docker & kubeadm ").lower()
        if user_input == "y":
            pass
        elif user_input == "n":
            print("退出程序")
            sys.exit()
        else:
            print("跳过安装 docker & kubeadm")
            print("程序继续执行")


if __name__ == "__main__":
    obj = Control()
