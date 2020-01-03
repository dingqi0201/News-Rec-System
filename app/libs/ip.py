# -*- coding:utf-8 -*-
"""
    ip.py
    ~~~~~~~~
    IP 相关助手函数

    :author: Fufu, 2019/12/26
"""
import ipaddress


def get_ip_address(ip=None):
    """
    检查是否为 IP 地址, 清除每个 IP 的空白, 返回 IP 字符串
    (单个 IPv4 或 IPv6)

    e.g.::

        # 127.0.0.1
        get_ip_address('127.0.0.1')

        # 0.0.0.10
        get_ip_address(10)

        # ::1
        get_ip_address('::1')

    :param ip: str
    :return:
    """
    try:
        return str(ipaddress.ip_address(ip))
    except ValueError:
        return None


def get_ips(ip=None, sep=None, fn='IPv4Address'):
    """
    检查是否为 IP 地址/网段/接口, 清除每个 IP 的空白, 返回 IP 字符串或 IP 列表

    e.g.::

        # 127.0.0.1
        get_ips(' 127.0.0.1   ')

        # 127.0.0.1
        get_ips(0x7f000001)

        # ['127.0.0.1', '8.8.8.8']
        get_ips('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ', ',')

        # ['::1', '2001:db8::']
        get_ips('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ,2001:db8::', ',', 'IPv6Address')

        # 0.0.0.10
        get_ips(10)

        # None
        get_ips('10')

        # 172.16.0.0/12
        get_ips('172.16.0.0/12', fn='IPv4Network')

        # 172.16.0.1/12
        get_ips('172.16.0.1/12', fn='IPv4Interface')

        # ['127.0.0.1/31', '8.8.8.8/24', '127.0.1.0/24']
        get_ips('127.0.0.1/31, 8.8.8.8/24,, 10a, 7,,127.0.1.0/24,::1 ', ',' , fn='IPv4Interface')

    :param ip: str, IP 地址
    :param sep: str, 指定分隔符时返回 list
    :param fn: str, ip_address / ip_network / ip_interface
    :return: str / list
    """
    if not ip:
        return None

    if sep:
        ret = []
        for x in ip.split(sep):
            ip_str = get_ips(x, fn=fn)
            if ip_str and ip_str not in ret:
                ret.append(ip_str)
    else:
        if isinstance(ip, str):
            ip = ip.strip()
        try:
            ret = str(getattr(ipaddress, fn)(ip))
        except Exception:
            ret = None

    return ret


def get_ipv6_address(ip=None, sep=None):
    """
    检查是否为 IPv6 地址, 清除每个 IP 的空白, 返回 IP 字符串或 IP 列表

    e.g.::

        # ::1
        get_ipv6_address('::1')

        # ['::1', '2001:db8::']
        get_ipv6_address('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ,2001:db8::', ',')

    :param ip: str, IP 地址
    :param sep: str, 指定分隔符时返回 list
    :return: str / list
    """
    return get_ips(ip, sep, fn='IPv6Address')


def get_ipv4_address(ip=None, sep=None):
    """
    检查是否为 IP 地址, 清除每个 IP 的空白, 返回 IP 字符串或 IP 列表

    e.g.::

        # 127.0.0.1
        get_ipv4_address(' 127.0.0.1   ')

        # 127.0.0.1
        get_ipv4_address(0x7f000001)

        # ['127.0.0.1', '8.8.8.8']
        get_ipv4_address('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ', ',')

        # 0.0.0.10
        get_ipv4_address(10)

    :param ip: str, IP 地址
    :param sep: str, 指定分隔符时返回 list
    :return: str / list
    """
    return get_ips(ip, sep, fn='IPv4Address')


def get_ipv4_network(ip=None, sep=None):
    """
    检查是否为 IP 网段, 清除每个 IP 的空白, 返回 IP 字符串或 IP 列表

    e.g.::

        # 172.16.0.0/12
        get_ipv4_network('172.16.0.0/12')

        # ['127.0.0.1/32', '8.8.8.8/32', '127.0.1.0/24']
        get_ipv4_network('127.0.0.1/32, 8.8.8.8,, 10a, 7,,127.0.1.0/24,::1 ', ',')

    :param ip: str, IP 地址
    :param sep: str, 指定分隔符时返回 list
    :return: str / list
    """
    return get_ips(ip, sep, fn='IPv4Network')


def get_ipv4_interface(ip=None, sep=None):
    """
    检查是否为 IP 接口, 清除每个 IP 的空白, 返回 IP 字符串或 IP 列表

    e.g.::

        # 172.16.0.1/12
        get_ipv4_interface('172.16.0.1/12')

        # ['127.0.0.1/31', '8.8.8.8/24', '127.0.1.0/24']
        get_ipv4_interface('127.0.0.1/31, 8.8.8.8/24,, 10a, 7,,127.0.1.0/24,::1 ', ',')

    :param ip: str, IP 地址
    :param sep: str, 指定分隔符时返回 list
    :return: str / list
    """
    return get_ips(ip, sep, fn='IPv4Interface')
