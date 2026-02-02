# -*- coding: utf-8 -*-
__author__ = 'hkhl'

import json
import tkinter as tk
import traceback
from tkinter import ttk

import pyperclip

from tool_funcs.json_extract import JsonExtractor


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
        # json路径取值输入框
        self.json_path_extract_entry = None
        # 转换指标参数按钮
        self.convert_button = None
        # 清除text内容按钮
        self.clear_text_button = None
        # 复制text内容按钮
        self.copy_text_button = None
        # 去重text内容按钮
        self.distinct_text_button = None
        # 转义text内容按钮 json.dumps
        self.escape_text_button = None
        # json路径取值按钮 json.dumps
        self.json_path_extract_button = None
        # text
        self.before_log_text = None
        self.after_log_text = None
        self.clear_log_button = None
        # const
        self.tab_name = '数据转换'
        self.sep_options = ['逗号', '制表符', '换行符', '无']
        self.sep_values = [',', '\t', '\n', '']
        self.convert_wrapper_options = ['单引号', '双引号', '无']
        self.convert_wrapper_values = ["'", '"', '']
        self.convert_sep_options = ['逗号', '制表符', '换行符', '无']
        self.convert_sep_values = [",", '\t', '\n', '']
        # 渲染布局
        self._create_ui()

    def _create_ui(self):
        """创建UI界面"""
        # 创建主框架
        self.tab = ttk.Frame(self.parent)

        # 创建三个主要区域
        self._create_top_frame()
        self._create_body_frame()
        self._create_tail_frame()

    def _create_top_frame(self):
        """创建顶部控制区域"""
        top_frame = ttk.Frame(self.tab)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # 第一行：下拉框区域
        dropdown_frame = ttk.Frame(top_frame)
        dropdown_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        self._create_dropdown_row(dropdown_frame)

        # 第二行：输入框区域
        entry_frame = ttk.Frame(top_frame)
        entry_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        self._create_entry_row(entry_frame)

        # 第三行：功能按钮区域
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        self._create_button_row(button_frame)

        # 第四行：文本域操作按钮区域
        text_button_frame = ttk.Frame(top_frame)
        text_button_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        self._create_text_button_row(text_button_frame)

    def _create_dropdown_row(self, parent):
        """创建下拉框行"""
        # 定义下拉框配置：(标签文本, 选项列表, 属性名)
        dropdowns = [
            ("分隔符：", self.sep_options, "sep_dropdown"),
            ("包裹符：", self.convert_wrapper_options, "convert_wrapper_dropdown"),
            ("转换间隔符：", self.convert_sep_options, "convert_sep_dropdown"),
        ]

        for idx, (label_text, options, attr_name) in enumerate(dropdowns):
            # 创建容器框架，让label和combobox成为一组
            group_frame = ttk.Frame(parent)
            group_frame.pack(side=tk.LEFT, padx=10)

            # 标签
            ttk.Label(group_frame, text=label_text).pack(side=tk.LEFT, padx=(0, 5))

            # 下拉框
            dropdown = ttk.Combobox(
                group_frame, width=12, state="readonly", values=options
            )
            dropdown.set(options[0])
            dropdown.pack(side=tk.LEFT)

            setattr(self, attr_name, dropdown)

    def _create_entry_row(self, parent):
        """创建下拉框行"""
        # 定义输入框
        entries = [
            ("路径：", "json_path_extract_entry"),
        ]

        for idx, (label_text, attr_name) in enumerate(entries):
            # 创建容器框架，让label和combobox成为一组
            group_frame = ttk.Frame(parent)
            group_frame.pack(side=tk.LEFT, padx=10)

            # 标签
            ttk.Label(group_frame, text=label_text).pack(side=tk.LEFT, padx=(0, 5))

            # 下拉框
            entry = ttk.Entry(group_frame, width=30)
            entry.pack(side=tk.LEFT)

            setattr(self, attr_name, entry)

    def _create_button_row(self, parent):
        """创建按钮行"""
        # 定义按钮配置：(文本, 命令, 属性名)
        buttons = [
            ("转换", self.convert_cmd, "convert_button"),
            ("去重", self.distinct_cmd, "distinct_text_button"),
            ("转义", self.escape_cmd, "escape_text_button"),
            ("路径取值", self.json_path_extract_cmd, "json_path_extract_button"),
        ]

        for text, command, attr_name in buttons:
            button = tk.Button(parent, text=text, command=command, width=10)
            button.pack(side=tk.LEFT, padx=5)
            setattr(self, attr_name, button)

    def _create_text_button_row(self, parent):
        """创建文本域按钮行"""
        # 定义按钮配置：(文本, 命令, 属性名)
        buttons = [
            ("清除", self.clear_text_cmd, "clear_text_button"),
            ("复制结果", self.copy_text_cmd, "copy_text_button"),
        ]

        for text, command, attr_name in buttons:
            button = tk.Button(parent, text=text, command=command, width=10)
            button.pack(side=tk.LEFT, padx=5)
            setattr(self, attr_name, button)

    def _create_body_frame(self):
        """创建中间文本输入区域"""
        body_frame = ttk.Frame(self.tab)
        body_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 创建转换前文本框
        self.before_log_text = self._create_text_widget(
            body_frame, state="normal"
        )

    def _create_tail_frame(self):
        """创建底部文本输出区域"""
        tail_frame = ttk.Frame(self.tab)
        tail_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 创建转换后文本框
        self.after_log_text = self._create_text_widget(
            tail_frame, state="disabled"
        )

    def _create_text_widget(self, parent, state="normal"):
        """创建带滚动条的文本框"""
        # 创建文本框
        text_widget = tk.Text(parent, width=140, height=10, state=state)

        # 创建滚动条
        scrollbar = tk.Scrollbar(parent)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 关联滚动条和文本框
        scrollbar.config(command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        return text_widget

    def get_tab(self):
        return self.tab

    def get_tab_name(self):
        return self.tab_name

    def distinct_cmd(self):
        self.convert_cmd(True)

    def json_path_extract_cmd(self):
        try:
            before_text = self.before_log_text.get("1.0", tk.END)
            json_path = self.json_path_extract_entry.get()
            if not before_text or not json_path:
                return
            before_text = before_text.strip()
            results = JsonExtractor.extract_values(before_text, json_path)

            wrapper = self.convert_wrapper_dropdown.get()
            convert_sep = self.convert_sep_dropdown.get()
            wrapper_index = self.convert_wrapper_options.index(wrapper)
            wrapper_value = self.convert_wrapper_values[wrapper_index]

            result_fields = ["{wrapper}{field}{wrapper}".format(field=field, wrapper=wrapper_value) for field in results]
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
            self.after_log_text.insert(tk.END, f"路径取值异常 {e}")
            self.after_log_text.config(state=tk.DISABLED)

    def escape_cmd(self):
        try:
            before_text = self.before_log_text.get("1.0", tk.END)
            if not before_text:
                return
            before_text = before_text.strip()
            params = json.dumps(before_text, ensure_ascii=False)
            # 去掉转义的双引号
            params = params[1:-1]
            self.after_log_text.config(state=tk.NORMAL)
            self.after_log_text.delete(1.0, tk.END)
            self.after_log_text.insert(tk.END, params)
            self.after_log_text.config(state=tk.DISABLED)
        except Exception as e:
            self.after_log_text.config(state=tk.NORMAL)
            self.after_log_text.delete(1.0, tk.END)
            self.after_log_text.insert(tk.END, f"转义异常 {e}")
            self.after_log_text.config(state=tk.DISABLED)

    def convert_cmd(self, distinct=False):
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
            elif seperator == self.sep_options[3]:
                fields = [before_text]
            else:
                sep_index = self.sep_options.index(seperator)
                fields = before_text.split(self.sep_values[sep_index])
            wrapper_index = self.convert_wrapper_options.index(wrapper)
            wrapper_value = self.convert_wrapper_values[wrapper_index]
            if distinct:
                # 去重
                distinct_fields = []
                for field in fields:
                    if field not in distinct_fields:
                        distinct_fields.append(field)
                fields = distinct_fields

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
            self.after_log_text.insert(tk.END, f"转换异常 {e}")
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


