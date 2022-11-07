import os
from subprocess import Popen
from starter.arg_data import VRAM_args, cmpt_args, GPU_args, component_args, bat_file, arg_line, update_file


def arg_bat(gpu_mode, vram_size, cmpt_mode, components):
    args_list = []
    kv_args = {gpu_mode: GPU_args, vram_size: VRAM_args, cmpt_mode: cmpt_args}
    for k1, v1 in kv_args.items():
        for k2, v2 in v1.items():
            if k1 == k2:
                if v2 != "":
                    args_list.append(v2)
                break
    for comp in components:
        for k1, v1 in component_args.items():
            if comp == k1:
                if v1 != "":
                    args_list.append(v1)
    args = ' '.join(args_list)
    print(args)

    with open(bat_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(bat_file, "w", encoding="utf-8") as f:
        for line in lines:
            if arg_line in line:
                line = arg_line + args + '\n'
            f.write(line)
    Popen(os.path.abspath(bat_file))


def update_bat():
    Popen(os.path.abspath(update_file))


def open_web(site):
    Popen("start " + site)
