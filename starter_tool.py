# coding:utf-8
import os
import tkinter
from tkinter import messagebox
import sv_ttk
import subprocess as sp

from starter.app import App, set_win_center
from starter.arg_data import VRAM_ranges, hypernetworks_dir, model_dir, emb_dir, extensions_dir


def ui(app_data, tree_data):
    root = tkinter.Tk()
    sv_ttk.set_theme("light")
    root.title('webui配置启动器1.0 @cynika')
    app = App(root, app_data, tree_data)
    app.bind_event()
    app.pack(expand=True, fill="both")

    root.update()
    set_win_center(root)
    root.resizable(False, False)  # 窗口不可调整大小

    root.lift()
    root.attributes('-topmost', True)  # 窗口弹出在最前
    root.attributes('-topmost', False)

    root.mainloop()


def run_cmd(cmd):
    cp = sp.run(cmd, shell=True, capture_output=True, encoding="utf-8")
    if cp.returncode != 0:
        error = f"""Something wrong has happened when running command [{cmd}]:{cp.stderr}"""
        raise Exception(error)
    return cp.stdout


def check_gpu():
    gpu_cmd = "nvidia-smi --format=csv,noheader,nounits --query-gpu=name"
    ram_cmd = "nvidia-smi --format=csv,noheader,nounits --query-gpu=memory.total"
    name = None
    ram = None
    mode = 1
    cmpt = 0
    try:
        name = run_cmd(gpu_cmd).replace("\n", "")
        ram = int(int(run_cmd(ram_cmd)) / 1024)
    except Exception as e:
        mode = 0
        print(e)

    size = [key for key, (low, high) in VRAM_ranges.items() if low <= ram <= high][0]
    if "16" in name:
        cmpt = 1
    return name, size, mode, cmpt, ram


def list_file():
    def listdir(i_dir):
        l_var = []
        try:
            l_var = os.listdir(os.path.abspath(i_dir))
        except Exception as e:
            print(e)
            l_var = []
        finally:
            return l_var

    model = listdir(model_dir)
    emb = listdir(emb_dir)
    hypernetworks = listdir(hypernetworks_dir)
    extensions = listdir(extensions_dir)
    file = model, emb, hypernetworks, extensions
    return file


if __name__ == "__main__":
    gpu_name, vram_size, gpu_mode, cmpt_16xx, ram = check_gpu()
    data = gpu_name, vram_size, gpu_mode, cmpt_16xx
    if gpu_mode == 1:
        messagebox.showinfo('提示', '已找到NVIDIA显卡\n' + gpu_name + ' ' + str(ram) + "GB")
    else:
        messagebox.showwarning('警告', '未找到NVIDIA显卡，请确保安装N卡及其驱动\n' + '已切换至CPU运算模式')
    files = list_file()
    ui(data, files)
