# -*- coding: utf-8 -*-
__author__ = 'hkhl'

import tkinter as tk
from tkinter import ttk
from tool_tabs import tool_data_tab


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


root = tk.Tk()
center_window(root, 800, 500)
root.title("tool v1.0")
# 创建一个Notebook控件
tab_control = ttk.Notebook(root)
# 将Notebook放置到窗口中
tab_control.pack(expand=1, fill="both")
root.iconbitmap(r"icons\favicon.ico")

# 创建标签页并添加到Notebook中
# 工具页tab
toolDataTab = tool_data_tab.ToolDataTab(root, tab_control)
tab_control.add(toolDataTab.get_tab(), text=toolDataTab.get_tab_name())

# 监听
root.mainloop()