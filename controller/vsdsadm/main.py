import os
import sys
import subprocess


def start_satellite():
    try:
        subprocess.run(["systemctl", "start", "linstor-satellite"], check=True)
        print("linstor-satellite服务已启动")
    except subprocess.CalledProcessError as e:
        print(f"启动linstor-satellite服务失败: {e}")
        sys.exit()

def start_controller():
    try:
        subprocess.run(["systemctl", "start", "linstor-controller"], check=True)
        print("linstor-controller服务已启动")
    except subprocess.CalledProcessError as e:
        print(f"启动linstor-controller服务失败: {e}")
        sys.exit()

def create_or_update_linstor_conf(controller_ip):
    conf_path = "/etc/linstor/linstor-client.conf"
    conf_content = f"[global]\ncontrollers={controller_ip}"

    os.makedirs(os.path.dirname(conf_path), exist_ok=True)
    try:
        with open(conf_path, 'w') as conf_file:
            conf_file.write(conf_content)
        print(f"lisntor-client.conf的controller ip更新为: {controller_ip}")
    except Exception as e:
        print(f"写入lisntor-client.conf时发生错误: {e}")


def append_fixed_content_to_file(password):
    filepath = '/etc/linstor/linstor.toml'
    content = f'\n[encrypt]\npassphrase="{password}"\n'
    try:
        with open(filepath, 'a') as file:
            file.write(content)
            print(f"lisntor.toml的密码更新为: {password}")
    except Exception as e:
        print(f"写入文件时发生错误: {e}")


def create_node(node_name,node_ip):
    try:
        subprocess.run(["linstor", "node", "create", node_name, node_ip, "--node-type", "Combined"], check=True)
        print(f"节点 {node_name} 已创建")
    except subprocess.CalledProcessError as e:
        print(f"节点 {node_name} 创建失败: {e}")
        sys.exit()


def adjusting_linstordb():
    node_info = subprocess.run(["linstor", "n", "l"], capture_output=True, text=True)
    if node_info.returncode != 0:
        print("命令 linstor n l 执行失败，错误信息如下：")
        print(node_info.stderr)


def adjusting_pvc():
    pass
def _count_nodes(info):
    lines = info.split('\n')
    node_count = 0
    for line in lines:
        if '┊' in line and 'Node' not in line:
            node_count += 1
    return node_count

def _count_linstordb(info):
    lines = info.split('\n')
    node_count = 0
    for line in lines:
        if '┊' in line and 'Node' not in line:
            node_count += 1
    return node_count

if __name__ == "__main__":
    pass