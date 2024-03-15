import os
import sys
import re
import subprocess
import yaml
import logging


def init_config(path="./config.yaml"):
    try:
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
        print("配置文件已成功加载")
        if (config['controller_ip'] is None or
                config['passphrase'] is None or
                config['local_node_name'] is None or
                config['device'] is None or
                config['local_node_ip'] is None):
            print(
                "警告：'controller_ip'、'passphrase'、'local_node_name'、’device‘或'local_node_ip'未配置，请检查config.yaml文件的填写。")
            sys.exit()
        return config
    except FileNotFoundError:
        print(f"文件{config.yaml}未找到")
    except yaml.YAMLError as e:
        print(f"解析YAML文件时出错: {e}")


def start_satellite():
    try:
        result = subprocess.run(["systemctl", "start", "linstor-satellite"], check=True)
        log_data = f"'localhost' - 'systemctl start linstor-satellite' - {result.stdout}"
        Log().logger.info(log_data)
        print("linstor-satellite服务已启动")
    except subprocess.CalledProcessError as e:
        print(f"启动linstor-satellite服务失败: {e}")
        sys.exit()


def start_controller():
    try:
        result = subprocess.run(["systemctl", "start", "linstor-controller"], check=True)
        log_data = f"'localhost' - 'systemctl start linstor-controller' - {result.stdout}"
        Log().logger.info(log_data)
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


def create_node(node_name, node_ip):
    try:
        result = subprocess.run(["linstor", "node", "create", node_name, node_ip, "--node-type", "Combined"], check=True)
        log_data = f"'localhost' - 'linstor node create {node_name} {node_ip} --node-type Combined' - {result.stdout}"
        Log().logger.info(log_data)
        print(f"节点 {node_name} 已创建")
    except subprocess.CalledProcessError as e:
        print(f"节点 {node_name} 创建失败: {e}")
        sys.exit()


def create_pv_vg_tp_sp(device, node_name):
    create_pv = subprocess.run(["pvcreate", device], capture_output=True, text=True)
    log_data = f"'localhost' - 'pvcreate {device}' - {create_pv.stdout}"
    Log().logger.info(log_data)
    if create_pv.returncode != 0:
        print(f"命令 pvcreate {device} 执行失败，错误信息如下：")
        print(create_pv.stderr)
        sys.exit()
    create_vg = subprocess.run(["vgcreate", "vg0", device], capture_output=True, text=True)
    log_data = f"'localhost' - 'vgcreate vg0 {device}' - {create_vg.stdout}"
    Log().logger.info(log_data)
    if create_vg.returncode != 0:
        print(f"命令 vgcreate vg0 {device} 执行失败，错误信息如下：")
        print(create_vg.stderr)
        sys.exit()
    create_lv = subprocess.run(["lvcreate", "-l", "+100%free", "--thinpool", "tp0", "vg0"], capture_output=True,
                               text=True)
    log_data = f"'localhost' - 'lvcreate -l +100%free --thinpool tp0 vg0' - {create_lv.stdout}"
    Log().logger.info(log_data)
    if create_lv.returncode != 0:
        print(f"命令lvcreate -l +100%free --thinpool tp0 vg0 执行失败，错误信息如下：")
        print(create_lv.stderr)
        sys.exit()
    create_sp = subprocess.run(["linstor", "sp", "c", "lvmthin", node_name, "thpool0", "vg0/tp0"], capture_output=True,
                               text=True)
    log_data = f"'localhost' - 'linstor sp c lvmthin {node_name} thpool0 vg0/tp0' - {create_sp.stdout}"
    Log().logger.info(log_data)
    if create_sp.returncode != 0:
        print(f"命令linstor sp c lvmthin {node_name} thpool0 vg0/tp0执行失败，错误信息如下：")
        print(create_sp.stderr)
        sys.exit()


def adjusting_linstordb():
    node_dict = _count_nodes()
    linstordb_list = _count_linstordb()
    nodes = list(node_dict.keys())
    if len(nodes) >= 3:
        if len(linstordb_list) < 3:
            d_node_dict = {key: value for key, value in node_dict.items() if key not in linstordb_list}
            keys = list(d_node_dict.keys())
            for i in range(3 - len(linstordb_list)):
                name = keys[i]
                sp = d_node_dict[name][0]
                create_res = subprocess.run(["linstor" "r" "c", name, "linstordb", "--storage-pool", sp],
                                            capture_output=True, text=True)
                log_data = f"'localhost' - 'linstor r c {name} linstordb --storage-pool {sp}' - {create_res.stdout}"
                Log().logger.info(log_data)
                if create_res.returncode != 0:
                    print(f"命令 linstor r c {name} linstordb --storage-pool {sp} 执行失败，错误信息如下：")
                    print(create_res.stderr)
                    sys.exit()
    else:
        if len(nodes) != len(linstordb_list):
            difference = [item for item in nodes if item not in linstordb_list]
            for i in difference:
                create_res = subprocess.run(["linstor" "r" "c", i, "linstordb", "--storage-pool", node_dict[i][0]],
                                            capture_output=True, text=True)
                log_data = f"'localhost' - 'linstor r c {i} linstordb --storage-pool {node_dict[i][0]}' - {create_res.stdout}"
                Log().logger.info(log_data)
                if create_res.returncode != 0:
                    print(f"命令 linstor r c {i} linstordb --storage-pool {node_dict[i][0]} 执行失败，错误信息如下：")
                    print(create_res.stderr)
                    sys.exit()


def adjusting_pvc():
    node_dict = _count_nodes()
    nodes = list(node_dict.keys())
    pvc_dict = _count_pvc()
    pvc_nodes = list(pvc_dict.keys())
    for pvc_name in pvc_nodes:
        if len(nodes) >= 3:
            if len(pvc_dict[pvc_name]) < 3:
                d_node_dict = {key: value for key, value in node_dict.items() if key not in pvc_dict[pvc_name]}
                keys = list(d_node_dict.keys())
                for i in range(3 - len(pvc_dict[pvc_name])):
                    name = keys[i]
                    sp = d_node_dict[name][0]
                    create_res = subprocess.run(["linstor" "r" "c", name, pvc_name, "--storage-pool", sp],
                                                capture_output=True, text=True)
                    log_data = f"'localhost' - 'linstor r c {name} linstordb --storage-pool {sp}' - {create_res.stdout}"
                    Log().logger.info(log_data)
                    if create_res.returncode != 0:
                        print(f"命令 linstor r c {name} {pvc_name} --storage-pool {sp} 执行失败，错误信息如下：")
                        print(create_res.stderr)
                        sys.exit()
        else:
            if len(nodes) != len(pvc_dict[pvc_name]):
                difference = [item for item in nodes if item not in pvc_dict[pvc_name]]
                for i in difference:
                    create_res = subprocess.run(["linstor" "r" "c", i, pvc_name, "--storage-pool", node_dict[i][0]],
                                                capture_output=True, text=True)
                    log_data = f"'localhost' - 'linstor r c {i} linstordb --storage-pool {node_dict[i][0]}' - {create_res.stdout}"
                    Log().logger.info(log_data)
                    if create_res.returncode != 0:
                        print(f"命令 linstor r c {i} {pvc_name} --storage-pool {node_dict[i][0]} 执行失败，错误信息如下：")
                        print(create_res.stderr)
                        sys.exit()


def _count_nodes():
    # 返回一个字典，为节点名和存储池的键值对
    sp_info = subprocess.run(["linstor", "sp", "l"], capture_output=True, text=True)
    data = sp_info.stdout
    pattern = r"\|\s*([\w\d]+)\s*\|\s*(\w+)\s*\|.*?\|\s*([\w\/]+)\s*\|"
    matches = re.findall(pattern, data)
    node_dict = {}
    for storage_pool, node, _ in matches:
        if storage_pool in ["StoragePool", "Node", "Driver", "PoolName", "FreeCapacity", "TotalCapacity",
                            "CanSnapshots", "State", "SharedName"]:
            continue
        if node not in node_dict:
            node_dict[node] = []
        if storage_pool != "DfltDisklessStorPool":
            node_dict[node].append(storage_pool)
    return node_dict


def _count_linstordb():
    # 返回一个数组，为有linstordb的节点名
    res_info = subprocess.run(["linstor", "r", "lv"], capture_output=True, text=True)
    data = res_info.stdout
    pattern = r"\|\s*(\w+)\s*\|\s*linstordb\s*\|"
    nodes = set(re.findall(pattern, data))
    return list(nodes)


def _count_pvc():
    # 返回一个字典，为有"pvc-"的资源名和节点名的键值对
    res_info = subprocess.run(["linstor", "r", "lv"], capture_output=True, text=True)
    data = res_info.stdout
    pattern = r"\|\s*(\w+)\s*\|\s*(pvc-\w+)\s*\|"
    matches = re.findall(pattern, data)
    result = {}
    for node, pvc in matches:
        if pvc in result:
            result[pvc].append(node)
        else:
            result[pvc] = [node]
    return result


class Log(object):
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            Log._instance = super().__new__(cls)
            Log._instance.logger = logging.getLogger()
            Log._instance.logger.setLevel(logging.INFO)
            Log.set_handler(Log._instance.logger)
        return Log._instance

    @staticmethod
    def set_handler(logger):
        fh = logging.FileHandler('./vsdsadm.log', mode='a')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)


if __name__ == "__main__":
    a = init_config()
    print(a)