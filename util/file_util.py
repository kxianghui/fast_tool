# -*- coding: utf-8 -*-
__author__ = 'hkhl'

import os


def read(path):
    """
    从指定路径文件获取内容
    :param path: 文件路径/文件名
    :return: String
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_binary(path, content):
    """
    写入二进制内容，覆盖
    :param path: 文件路径
    :param content: 写入二进制内容
    :return:
    """
    with open(path, 'wb') as f:
        f.write(content)





