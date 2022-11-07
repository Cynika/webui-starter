# coding:utf-8

import tkinter
from tkinter import ttk

from starter.arg_data import VRAM_args, cmpt_args, component_args
from starter.bat import arg_bat, update_bat, open_web

VRAM_list = list(VRAM_args.keys())
cmpt_list = list(cmpt_args.keys())
component_list = list(component_args.keys())


def set_win_center(root):
    """
    设置窗口大小，并居中显示
    :param root:主窗体实例
    """
    width = root.winfo_width()
    height = root.winfo_height()

    # 获取屏幕宽度和高度
    scn_w, scn_h = root.maxsize()

    # 计算中心坐标
    cen_x = (scn_w - width) / 2
    cen_y = (scn_h - height) / 2

    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (width, height, cen_x, cen_y)
    root.geometry(size_xy)


class CheckBoxs(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="组件启动项", padding=10)
        self.vars = {}
        for key in component_list:
            self.vars.update({key: tkinter.IntVar()})

        self.add_widgets()

    def add_widgets(self):
        n = 0
        for key, value in self.vars.items():
            ttk.Checkbutton(self, text=key, variable=value).grid(row=n, column=0, padx=(0, 5), pady=5, sticky="w")
            n = n + 1

        self.button = ttk.Button(self, text="deepdanbooru\n需安装CUDA驱动")
        self.button.grid(row=n, column=0, padx=5, pady=5, sticky="nsew")


class RadioButtons(ttk.LabelFrame):
    def __init__(self, parent, data):
        super().__init__(parent, text="运算硬件模式", padding=10)

        self.gpu_mode = tkinter.IntVar()
        self.data = data
        self.gpu_mode.set(0)

        self.add_widgets()

        if self.data[2] == 1:
            self.gpu_mode.set(1)

    def add_widgets(self):
        self.radio_1 = ttk.Radiobutton(self, text="Nvdia显卡(GPU)", variable=self.gpu_mode, value=1)
        self.radio_1.grid(row=0, column=0, pady=(0, 5), sticky="w")

        self.radio_2 = ttk.Radiobutton(self, text="无显卡/A卡(CPU)", variable=self.gpu_mode, value=0)
        self.radio_2.grid(row=1, column=0, pady=(0, 5), sticky="w")


class Buttons(ttk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent, style="Card.TFrame", padding=20)

        self.columnconfigure(0, weight=1)
        self.data = data
        self.name = tkinter.StringVar()
        self.vram_size = tkinter.StringVar()
        self.cmpt_mode = tkinter.StringVar()

        self.name.set("未找到NVIDIA显卡")
        self.vram_size.set("无有效显存")
        self.cmpt_mode.set("正常模式(无需兼容)")

        if self.data[2] == 1:
            self.name.set(self.data[0])
            self.vram_size.set(self.data[1])
        if self.data[3] == 1:
            self.cmpt_mode.set("16xx显卡兼容模式")

        self.add_widgets()

    def add_widgets(self):

        self.entry = ttk.Entry(self, textvariable=self.name)
        self.entry.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")

        self.combobox1 = ttk.Combobox(self, state="readonly", textvariable=self.vram_size, values=VRAM_list)
        self.combobox1.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        self.readonly2 = ttk.Combobox(self, state="readonly", textvariable=self.cmpt_mode, values=cmpt_list)
        self.readonly2.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        self.togglebutton = ttk.Checkbutton(self, text="配置并启动 webUI !", style="Toggle.TButton")
        self.togglebutton.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

        self.separator = ttk.Separator(self)
        self.separator.grid(row=5, column=0, pady=5, sticky="ew")

        self.accentbutton1 = ttk.Button(self, text=" 更新webUI(可能需代理)", style="Accent.TButton")
        self.accentbutton1.grid(row=6, column=0, padx=5, pady=10, sticky="ew")

        self.accentbutton2 = ttk.Button(self, text="信息并联计划(社群,工具站)", style="Accent.TButton")
        self.accentbutton2.grid(row=7, column=0, padx=5, pady=10, sticky="ew")


class Paned(ttk.PanedWindow):
    def __init__(self, parent, tree_data):
        super().__init__(parent)

        self.tree_data = tree_data
        self.add_widgets()

    def add_widgets(self):
        self.pane_1 = ttk.Frame(self, padding=(0, 0, 5, 5))
        self.add(self.pane_1, weight=1)

        self.scrollbar1 = ttk.Scrollbar(self.pane_1)
        self.scrollbar1.pack(side="right", fill="y")

        self.tree1 = ttk.Treeview(
            self.pane_1,
            height=5,
            selectmode="browse",
            show=("tree",),
            yscrollcommand=self.scrollbar1.set,
        )

        self.scrollbar1.config(command=self.tree1.yview)
        self.tree1.pack(expand=True, fill="both")
        self.tree1.column("#0", anchor="w", width=150)

        tree_data = [
            ("", 1, "model", []),
            ("", 2, "embeddings", []),
            ("", 3, "hypernetworks", []),
            ("", 4, "extensions", []),
            *[(1, x, x, []) for x in self.tree_data[0]],
            *[(2, x, x, []) for x in self.tree_data[1]],
            *[(3, x, x, []) for x in self.tree_data[2]],
            *[(4, x, x, []) for x in self.tree_data[3]]
        ]
        for item in tree_data:
            parent, iid, text, values = item
            try:
                self.tree1.insert(parent=parent, index="end", iid=iid, text=text, values=values)
            except Exception as e:
                print(e)


class More(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=5)

        self.add_widgets()

    def add_widgets(self):
        self.morebutton = ttk.Checkbutton(self, text="获取更多model,pt,prompt", style="Toggle.TButton")
        self.morebutton.grid(row=0, column=0, padx=0, pady=5, sticky="ew")


class App(ttk.Frame):
    def __init__(self, parent, data, tree_data):
        super().__init__(parent, padding=15)

        for index in range(2):
            self.columnconfigure(index, weight=1)
            self.rowconfigure(index, weight=1)

        self._CheckBox = CheckBoxs(self)
        self._RadioButton = RadioButtons(self, data)
        self._Button = Buttons(self, data)
        self._Paned = Paned(self, tree_data)
        self._more = More(self)
        self._RadioButton.grid(row=0, column=0, rowspan=2, padx=10, pady=(10, 0), sticky="new")
        self._CheckBox.grid(row=1, column=0, rowspan=1, padx=10, pady=(0, 10), sticky="sew")
        self._Button.grid(row=0, column=1, rowspan=2, padx=10, pady=(10, 10), sticky="ns")
        self._Paned.grid(row=0, column=3, rowspan=2, padx=10, pady=(10, 10), sticky="nsw")
        self._more.grid(row=1, column=3, rowspan=1, padx=10, pady=(10, 10), sticky="sew")

    def start_webui(self, event):
        component = []
        for key, value in self._CheckBox.vars.items():
            if value.get() == 1:
                component.append(key)
        gpu_mode = str(self._RadioButton.gpu_mode.get())
        vram_size = self._Button.vram_size.get()
        cmpt_mode = self._Button.cmpt_mode.get()
        arg_bat(gpu_mode, vram_size, cmpt_mode, component)

    @staticmethod
    def update_webui(event):
        update_bat()

    @staticmethod
    def doc(event):
        open_web("https://www.kdocs.cn/l/cre0TwbMkdx3?from=docs")

    @staticmethod
    def cuda(event):
        open_web("http://https://developer.nvidia.com/cuda-downloads")

    @staticmethod
    def more(event):
        open_web("https://space.bilibili.com/3089593/article")

    def bind_event(self):
        self._Button.togglebutton.bind('<Button-1>', self.start_webui)
        self._Button.accentbutton1.bind('<Button-1>', self.update_webui)
        self._Button.accentbutton2.bind('<Button-1>', self.doc)
        self._CheckBox.button.bind('<Button-1>', self.cuda)
        self._more.morebutton.bind('<Button-1>', self.more)
