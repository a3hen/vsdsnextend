import sys
import os
import subprocess
from controller import vsdsadm



def check_root():
    if os.geteuid() != 0:
        print("此脚本需要 root 权限运行。请以 root 用户执行此操作。")
        sys.exit(1)


class Control:
    def __init__(self):
        self.main()

    def main(self):
        check_root()
        print("节点拓展程序")
        print("* * * * * * * * * * * * * * * *")
        print("  请选择要执行的操作(0~12)，按其他键退出程序:")
        print("  0: * 替换内核操作")
        print("  1: * 顺序执行配置流程")
        print("  2: 安装和配置network manager")
        print("  3: 配置网络")
        print("  4: 实现ssh免密")
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
        if user_input == '0':
            pass
        elif user_input == '1':
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

    def replacement_kernel_check(self):
        user_input = input("是否按照要求替换好内核 (y/n)，按其他键退出程序: ").lower()
        if user_input == 'y':
            print("已替换好内核，即将安装软件")
        elif user_input.lower() == 'n':
            print("请先替换内核，再安装软件")
        else:
            print("请先替换内核，再安装软件")
            sys.exit()

    def replacement_kernel(self):
        user_input = input("是否开始替换内核 (y/n)，按其他键退出程序: ").lower()
        if user_input == 'y':
            try:
                subprocess.run(['python', '-m', 'controller.vsdsinstaller_k.main', '-r'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"vsdsinstaller_k -r 失败: {e}")
                sys.exit()
            print("已替换好内核，需要重启系统，并选择此内核启动")
        elif user_input.lower() == 'n':
            print("退出程序")
            sys.exit()
        else:
            print("退出程序")
            sys.exit()

    def vsdsipconf(self):
        print("安装网络配置工具，若已安装可跳过")
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过安装网络配置: ").lower()
        if user_input == 'y':
            try:
                subprocess.run(['python', '-m', 'controller.vsdsipconf.main'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"安装网络配置工具失败: {e}")
                sys.exit()
        elif user_input.lower() == 'n':
            print("请先填写配置文件")
            print("退出程序")
            sys.exit()
        else:
            print("退出网络配置工具安装")
            print("程序继续执行")

    def vsdsiptool(self):
        print("ip 配置，若已配置 ip 可跳过")
        user_input = input("是否跳过 ip 配置 (y/n)，按其他键跳过 ip 配置: ").lower()
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
                    device1 = input("网络接口1（子网卡1）: ")
                    device2 = input("网络接口2（子网卡2）: ")
                    mode = input("bonding 模式: ")
                    try:
                        subprocess.run(['python','-m','controller.vsdsiptool.main','bonding','create',bond_name,'-ip',ip,'-d',device1,device2,'-m',mode], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"配置Bonding网络失败: {e}")
                        sys.exit()
                    break
                elif choose_input == '2':
                    print("请输入 ip 和 网络接口（网卡）")
                    ip = input("ip: ")
                    device = input("网络接口（网卡）: ")
                    try:
                        subprocess.run(['python','-m','controller.vsdsiptool.main','ip','create','-ip',ip,'-d',device], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"配置普通网络失败: {e}")
                        sys.exit()
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
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过 ssh 免密配置: ").lower()
        if user_input == "y":
            try:
                subprocess.run(['python', '-m', 'controller.vsdssshfree.main', '-m'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"sshfree -m 失败: {e}")
                sys.exit()
            try:
                subprocess.run(['python', '-m', 'controller.vsdssshfree.main', 'fe'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"sshfree fe 失败: {e}")
                sys.exit()
        elif user_input == "n":
            print("请先填写配置文件")
            print("退出程序")
        else:
            print("跳过 ssh 免密配置")
            print("程序继续执行")

    # 执行vsdsinstaller-k -i，安装 DRBD/LINSTOR
    def vsdsinstaller_k(self):
        print("安装DRBD/LINSTOR，若已安装可跳过")
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过 DRBD/LINSTOR 安装: ").lower()
        if user_input == "y":
            try:
                subprocess.run(['python', '-m', 'controller.vsdsinstaller_k.main', '-i'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"vsdsinstaller_k -i 失败: {e}")
                sys.exit()
            try:
                subprocess.run(['python', '-m', 'controller.vsdsinstaller_k.main', '-t'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"vsdsinstaller_k -t 失败: {e}")
                sys.exit()
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
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过高可用软件安装: ").lower()
        if user_input == "y":
            try:
                subprocess.run(['python', '-m', 'controller.vsdsinstaller_u.main', '-u'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"vsdsinstaller_u -i 失败: {e}")
                sys.exit()
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
        user_input = input("是否进行 VersaSDS 预配置 (y/n)，按其他键跳过 VersaSDS 预配置: ").lower()
        if user_input == "y":
            try:
                subprocess.run(['python', '-m', 'controller.vsdspreset.main'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"vsdspreset 失败: {e}")
                sys.exit()
        elif user_input == "n":
            print("退出程序")
            sys.exit()
        else:
            print("跳过 VersaSDS 预配置")
            print("程序继续执行")

    # 执行vsdsadm，配置 LVM 和 LINSTOR 集群
    def vsdsadm(self):
        print("配置 LVM 和 LINSTOR 集群，如已配置可以跳过")
        user_input = input("是否配置 LVM 和 LINSTOR 集群 (y/n)，按其他键跳过配置 LVM 和 LINSTOR 集群").lower()
        if user_input == "y":
            config_list = vsdsadm.main.init_config(path="controller/vsdsadm/vsdsadm_config.yaml")
            # 配置linstor-client.conf
            vsdsadm.main.create_or_update_linstor_conf(controller_ip=config_list['controller_ip'])
            # 配置linstor.toml
            vsdsadm.main.append_fixed_content_to_file(password=config_list['passphrase'])
            # 开启satellite
            vsdsadm.main.start_satellite()
            # 创建新节点
            vsdsadm.main.create_node(node_name=config_list[
            'local_node_name'], node_ip=config_list[
            'local_node_ip'])
            # 创建lvm、存储池
            vsdsadm.main.create_pv_vg_tp_sp(device=config_list['device'],node_name=['local_node_name'])
            # 调整 linstordb 副本
            vsdsadm.main.adjusting_linstordb()
            # 调整 PVC 副本
            vsdsadm.main.adjusting_pvc()
        elif user_input == "n":
            print("退出程序")
            sys.exit()
        else:
            print("跳过配置 LVM 和 LINSTOR 集群")
            print("程序继续执行")

    def vsdscoroconf(self):
        print("配置 Corosync，如已配置可以跳过")
        user_input = input("是否已填写配置文件 (y/n)，按其他键跳过 Corosync 配置: ").lower()
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
        user_input = input("是否执行配置 (y/n)，按其他键跳过高可用配置: ").lower()
        if user_input == "y":
            try:
                subprocess.run(['python', '-m', 'controller.vsdshaconf.main', 'exetnd'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"vsdshaconf 失败: {e}")
                sys.exit()
        elif user_input == "n":
            print("退出程序")
            sys.exit()
        else:
            print("跳过高可用配置")
            print("程序继续执行")

    def csmpreinstaller(self):
        print("安装 docker & kubeadm 等软件")
        user_input = input("是否执行安装 (y/n)，按其他键跳过安装 docker & kubeadm: ").lower()
        if user_input == "y":
            if user_input == "y":
                try:
                    subprocess.run(['python', '-m', 'controller.csmpreinstaller.main'], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"安装 docker & kubeadm 等软件 失败: {e}")
                    sys.exit()
        elif user_input == "n":
            print("退出程序")
            sys.exit()
        else:
            print("跳过安装 docker & kubeadm")
            print("程序继续执行")


if __name__ == "__main__":
    obj = Control()
