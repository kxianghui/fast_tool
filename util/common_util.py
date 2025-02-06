# -*- coding: utf-8 -*-
__author__ = 'hkhl'

import socket


def compare(lines_1, lines_2, print_line=True):
    """
    lines_1有多少行不在lines_2中
    :param lines_1:
    :param lines_2:
    :return:
    """
    not_exist_lines = []
    for line in lines_1:
        if line not in lines_2:
            not_exist_lines.append(line)
    if print_line:
        for line in not_exist_lines:
            print(line)
    else:
        return not_exist_lines


def snake_to_camel_case(snake_case_string):
    """
    蛇形转驼峰
    :param snake_case_string:
    :return:
    """
    words = snake_case_string.split('_')
    camel_case_string = words[0].lower() + ''.join(word.title() for word in words[1:])
    return camel_case_string


def get_ip_host_info(hostname):
    """
    根据host获取ip 确定环境
    :param hostname:
    :param print_line:
    :return:
    """
    ip = socket.gethostbyname(hostname)
    return "hostname:{}, ip:{}".format(hostname, ip)

def get_ip_by_host(hostname):
    """
    根据host获取ip 确定环境
    :param hostname:
    :param print_line:
    :return:
    """
    return socket.gethostbyname(hostname)


def convert_to_bytes(size):
    """
    字符转字节
    :param size:
    :return:
    """
    size_value = size[:-2]
    size_unit = size[-2:].upper()

    try:
        value = float(size_value)

        if size_unit == 'KB':
            bytes_result = int(value * 1024)
        elif size_unit == 'MB':
            bytes_result = int(value * 1024 * 1024)
        elif size_unit == 'GB':
            bytes_result = int(value * 1024 * 1024 * 1024)
        else:
            print("Unsupported unit:", size_unit)
            return None

        return bytes_result
    except ValueError:
        print("Invalid size value:", size_value)
        return None