# -*- coding: utf-8 -*-
__author__ = 'hkhl'

import tkinter as tk
from queue import Queue
from util import date_util

class TextLogOutput(object):

    def __init__(self, root, text_widget, source):
        self.root = root
        self.text_widget = text_widget
        self.source = source
        self.log_queue = Queue()
        self.log_template = '{time} [{level}] [{source}] - {log}\n'

        # 开启监听
        self.run()

    def info(self, log_content):
        self.__append('INFO', log_content)

    def warn(self, log_content):
        self.__append('WARN', log_content)

    def error(self, log_content):
        self.__append('ERROR', log_content)

    def __append(self, level, log_content):
        real_content = self.log_template.format(time=date_util.format_now(), level=level, source=self.source, log=log_content)
        self.log_queue.put(real_content)

    def clear(self):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def run(self):
        while not self.log_queue.empty():
            log_content = self.log_queue.get()
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.insert(tk.END, log_content)
            self.text_widget.config(state=tk.DISABLED)
        # 继续调度下一次更新
        self.root.after(100, self.run)