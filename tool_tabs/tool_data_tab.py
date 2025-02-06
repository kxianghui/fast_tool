# -*- coding: utf-8 -*-
__author__ = 'hkhl'

import tkinter
import tkinter as tk
import traceback
from tkinter import ttk

import pyperclip


class ToolDataTab(object):
    """
    统一数据同步数据相关工具
    同步数据参数：提示标签*1、文本输入框*1
    同步按钮：按钮*1
    域名环境检测：域名下拉列表框*1 域名ip获取按钮*1
    """

    def __init__(self, root, parent):
        self.root = root
        # tab control
        self.parent = parent
        # 分隔符下拉
        self.sep_dropdown = None
        # 转换后包裹符号下拉
        self.convert_wrapper_dropdown = None
        # 转换后间隔符号下拉
        self.convert_sep_dropdown = None
        # 转换指标参数按钮
        self.convert_button = None
        # 清除text内容按钮
        self.clear_text_button = None
        # 复制text内容按钮
        self.copy_text_button = None
        # text
        self.before_log_text = None
        self.after_log_text = None
        self.clear_log_button = None
        # const
        self.tab_name = '数据转换'
        self.sep_options = ['逗号', '制表符', '换行符']
        self.sep_values = [',', '\t', '\n']
        self.convert_wrapper_options = ['单引号', '双引号', '无']
        self.convert_wrapper_values = ["'", '"', '']
        self.convert_sep_options = ['逗号', '制表符', '换行符']
        self.convert_sep_values = [",", '\t', '\n']
        # 渲染布局
        self.__layout()

    def __layout(self):
        # 创建一个Notebook控件
        self.tab = ttk.Frame(self.parent)
        top_frame = ttk.Frame(self.tab)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        body_frame = ttk.Frame(self.tab)
        body_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        tail_frame = ttk.Frame(self.tab)
        tail_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 分隔符下拉框
        self.sep_dropdown = ttk.Combobox(top_frame, width=6, state="readonly", values=self.sep_options)
        self.sep_dropdown.set(self.sep_options[0])  # 默认选择第一个选项
        self.sep_dropdown.grid(row=0, column=0, ipadx=10, pady=5)
        # 转换后包裹符号下拉框
        self.convert_wrapper_dropdown = ttk.Combobox(top_frame, width=6, state="readonly", values=self.convert_wrapper_options)
        self.convert_wrapper_dropdown.set(self.convert_wrapper_options[0])  # 默认选择第一个选项
        self.convert_wrapper_dropdown.grid(row=0, column=1, ipadx=10, pady=5)
        # 转换后间隔符号下拉框
        self.convert_sep_dropdown = ttk.Combobox(top_frame, width=6, state="readonly", values=self.convert_sep_options)
        self.convert_sep_dropdown.set(self.convert_sep_options[0])  # 默认选择第一个选项
        self.convert_sep_dropdown.grid(row=0, column=2, ipadx=10, pady=5)

        # 按钮
        self.convert_button = tk.Button(top_frame, text="转换", command=self.convert_cmd)
        self.convert_button.grid(row=1, column=0, pady=5, ipadx=10, sticky="W")
        self.clear_text_button = tk.Button(top_frame, text="清除", command=self.clear_text_cmd)
        self.clear_text_button.grid(row=1, column=1, ipadx=10, sticky="W")
        self.copy_text_button = tk.Button(top_frame, text="复制结果", command=self.copy_text_cmd)
        self.copy_text_button.grid(row=1, column=2, ipadx=10, sticky="W")

        # 转换前文本框
        self.before_log_text = tk.Text(body_frame, width=140, height=10, state="normal")
        before_scroll = tkinter.Scrollbar(body_frame)
        before_scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.before_log_text.pack(side=tkinter.LEFT, fill=tkinter.Y)
        before_scroll.config(command=self.before_log_text.yview)
        self.before_log_text.config(yscrollcommand=before_scroll.set)

        # 转换后文本框
        self.after_log_text = tk.Text(tail_frame, width=140, height=10, state="disabled")
        after_scroll = tkinter.Scrollbar(tail_frame)
        after_scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.after_log_text.pack(side=tkinter.LEFT, fill=tkinter.Y)
        after_scroll.config(command=self.after_log_text.yview)
        self.after_log_text.config(yscrollcommand=after_scroll.set)

    def get_tab(self):
        return self.tab

    def get_tab_name(self):
        return self.tab_name

    def convert_cmd(self):
        try:
            before_text = self.before_log_text.get("1.0", tk.END)
            if not before_text:
                return
            before_text = before_text.strip()
            seperator = self.sep_dropdown.get()
            wrapper = self.convert_wrapper_dropdown.get()
            convert_sep = self.convert_sep_dropdown.get()
            #self.sep_options = [',', '制表符', '换行符']
            # self.convert_wrapper_options = ['单引号', '双引号']
            if seperator == self.sep_options[2]:
                fields = before_text.splitlines()
            else:
                sep_index = self.sep_options.index(seperator)
                fields = before_text.split(self.sep_values[sep_index])
            wrapper_index = self.convert_wrapper_options.index(wrapper)
            wrapper_value = self.convert_wrapper_values[wrapper_index]
            result_fields = ["{wrapper}{field}{wrapper}".format(field=field, wrapper=wrapper_value) for field in fields]

            convert_sep_index = self.convert_sep_options.index(convert_sep)
            convert_sep_value = self.convert_sep_values[convert_sep_index]
            params = convert_sep_value.join(result_fields)
            self.after_log_text.config(state=tk.NORMAL)
            self.after_log_text.delete(1.0, tk.END)
            self.after_log_text.insert(tk.END, params)
            self.after_log_text.config(state=tk.DISABLED)
        except Exception as e:
            self.after_log_text.config(state=tk.NORMAL)
            self.after_log_text.delete(1.0, tk.END)
            self.after_log_text.insert(tk.END, "转换异常 {}".format(traceback.format_exc()))
            self.after_log_text.config(state=tk.DISABLED)

    def clear_text_cmd(self):
        self.before_log_text.delete(1.0, tk.END)
        self.after_log_text.config(state=tk.NORMAL)
        self.after_log_text.delete(1.0, tk.END)
        self.after_log_text.config(state=tk.DISABLED)

    def copy_text_cmd(self):
        after_text = self.after_log_text.get("1.0", tk.END)
        if after_text:
            after_text = after_text[:-1]
        pyperclip.copy(after_text)


