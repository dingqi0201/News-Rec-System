#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    test_get_ips.py
    ~~~~~~~~

    2020/12/26
"""
try:
    import __init__
except ModuleNotFoundError:
    import tests.__init__

import unittest

from app.libs.ip import get_ip_address, get_ips, get_ipv4_address, get_ipv6_address


class TestGetInt(unittest.TestCase):

    def test_get_ips(self):
        self.assertEqual(get_ips(' 127.0.0.1   '), '127.0.0.1')
        self.assertEqual(get_ips(0x7f000001), '127.0.0.1')
        self.assertEqual(get_ip_address(0x7f000001), '127.0.0.1')
        self.assertEqual(get_ipv4_address(0x7f000001), '127.0.0.1')

        # ['127.0.0.1', '8.8.8.8']
        self.assertEqual(get_ipv4_address('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ', ','),
                         ['127.0.0.1', '8.8.8.8'])
        self.assertEqual(get_ips('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ', ','),
                         ['127.0.0.1', '8.8.8.8'])

        # ['::1', '2001:db8::']
        self.assertEqual(get_ipv6_address('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ,2001:db8::', ','),
                         ['::1', '2001:db8::'])
        self.assertEqual(get_ips('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ,2001:db8::', ',', 'IPv6Address'),
                         ['::1', '2001:db8::'])

        # 0.0.0.10
        self.assertEqual(get_ips(10), '0.0.0.10')

        # 172.16.0.0/12
        self.assertEqual(get_ips('172.16.0.0/12', fn='IPv4Network'), '172.16.0.0/12')

        # 172.16.0.1/12
        self.assertEqual(get_ips('172.16.0.1/12', fn='IPv4Interface'), '172.16.0.1/12')

        # ['127.0.0.1/31', '8.8.8.8/24', '127.0.1.0/24']
        self.assertEqual(get_ips('127.0.0.1/31, 8.8.8.8/24,, 10a, 7,,127.0.1.0/24,::1 ', ',', fn='IPv4Interface'),
                         ['127.0.0.1/31', '8.8.8.8/24', '127.0.1.0/24'])

    def test_error(self):
        self.assertEqual(get_ips('a123, 4.56,, x,, ,', sep=','), [])
        self.assertEqual(get_ips(None, sep=','), None)
        self.assertEqual(get_ips(None), None)
        self.assertEqual(get_ips('10'), None)

    def test_ip_address(self):
        self.assertEqual(get_ip_address('1.1.1.1'), '1.1.1.1')
        self.assertEqual(get_ip_address('::1'), '::1')
        self.assertEqual(get_ipv6_address('::1'), '::1')
        self.assertEqual(get_ip_address(10), '0.0.0.10')


if __name__ == '__main__':
    unittest.main()
