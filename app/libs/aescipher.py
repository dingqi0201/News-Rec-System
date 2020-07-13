# -*- coding:utf-8 -*-
"""
    aescipher.py
    ~~~~~~~~
    AES_128_CBC, AES_192_CBC, AES_256_CBC
    pycryptodome==3.9.8

    e.g.::

        my_aes_bit = 256
        my_data = 123.05
        my_key = b'ff\xf4YF7777777\x024\x66~\xa7\xb6\x5c12356'
        my_iv = 'xyz1234abc1234'
        my_key_hex = AESCipher.mk_key(my_key, int(my_aes_bit / 8)).hex()
        my_iv_hex = AESCipher.mk_key(my_iv, AES.block_size).hex()
        print(f'my_key: {my_key}\nmy_iv: {my_iv}\n')
        print(f'my_key_hex: {my_key_hex}\nmy_iv_hex: {my_iv_hex}\n')

        encrypted_data, encrypted_key, encrypted_iv = encrypt_aes_cbc_hex(my_data, my_key, my_iv)
        print(f'encrypted: {encrypted_data}\nkey_hex: {encrypted_key}\niv_hex: {encrypted_iv}\n')

        print(decrypt_aes_cbc_hex(encrypted_data, encrypted_key, encrypted_iv).decode())
        print(decrypt_aes_cbc_hex(encrypted_data, my_key_hex, my_iv_hex).decode())
        print(decrypt_aes_cbc_hex_src(encrypted_data, my_key, my_iv).decode())

    :author: Fufu, 2019/11/5
"""
from Crypto.Cipher import AES
from Crypto.Util import Padding
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode


def encrypt_aes_cbc(data_src, key=None, iv=None, bits=256):
    return AESCipher().encrypt_aes_cbc(data_src, key, iv, bits).result()


def encrypt_aes_cbc_base64(data_src, key=None, iv=None, bits=256):
    return AESCipher().encrypt_aes_cbc(data_src, key, iv, bits).base64()


def encrypt_aes_cbc_hex(data_src, key=None, iv=None, bits=256):
    return AESCipher().encrypt_aes_cbc(data_src, key, iv, bits).hex()


def decrypt_aes_cbc(encrypted, key, iv):
    return AESCipher.decrypt_aes_cbc(encrypted, key, iv)


def decrypt_aes_cbc_base64(encrypted, key, iv):
    return AESCipher.decrypt_aes_cbc(b64decode(encrypted), b64decode(key), b64decode(iv))


def decrypt_aes_cbc_hex(encrypted, key, iv):
    return AESCipher.decrypt_aes_cbc(bytes.fromhex(encrypted), bytes.fromhex(key), bytes.fromhex(iv))


def decrypt_aes_cbc_src(encrypted, key, iv):
    return AESCipher.decrypt_aes_cbc_src(encrypted, key, iv)


def decrypt_aes_cbc_base64_src(encrypted, key, iv):
    return AESCipher.decrypt_aes_cbc_src(b64decode(encrypted), key, iv)


def decrypt_aes_cbc_hex_src(encrypted, key, iv):
    return AESCipher.decrypt_aes_cbc_src(bytes.fromhex(encrypted), key, iv)


class AESCipher:
    """
    AES 加密解密

    e.g.::

        data_src = ' fufu.中$'

        # 助手函数, 三种返回值
        encrypted, key, iv = encrypt_aes_cbc(data_src)
        encrypted, key, iv = encrypt_aes_cbc_hex(data_src)
        encrypted, key, iv = encrypt_aes_cbc_base64(data_src)

        # 解密, 对应三种返回值的加密结果
        data = decrypt_aes_cbc_base64(encrypted, key, iv).decode()

        # 指定 key, iv 等参数, bits = 128, 192, 256 => aes-128-cbc, aes-192-cbc, aes-256-cbc(缺省)
        res = AESCipher().encrypt_aes_cbc(data_src, 'my key', 'iv', 128)
        res = AESCipher().encrypt_aes_cbc(data_src, bits=192)

    """

    def __init__(self):
        self.data = None
        self.key = None
        self.iv = None

    def encrypt_aes_cbc(self, data_src, key=None, iv=None, bits=256):
        # key 长度, 16, 24, 32
        self.key = AESCipher.mk_key(key, int(bits / 8))
        self.iv = AESCipher.mk_key(iv, AES.block_size)
        self.data = AES.new(self.key, AES.MODE_CBC, iv=self.iv).encrypt(AESCipher.mk_pad_bytes(data_src))

        return self

    def result(self):
        return self.data, self.key, self.iv

    def hex(self):
        """
        返回值为 hex

        e.g.::

            encrypt_aes_cbc_hex('data123')
            AESCipher().encrypt_aes_cbc('data123').hex()

        :return: tuple
        """
        return self.data.hex(), self.key.hex(), self.iv.hex()

    def base64(self):
        """
        返回值为 hex

        e.g.::

          encrypt_aes_cbc_base64('data123')
          AESCipher().encrypt_aes_cbc('data123').base64()

        :return: tuple
        """
        return b64encode(self.data), b64encode(self.key), b64encode(self.iv)

    @staticmethod
    def decrypt_aes_cbc(encrypted, key, iv):
        key = AESCipher.mk_bytes(key)
        iv = AESCipher.mk_bytes(iv)
        res = AES.new(key, AES.MODE_CBC, iv=iv).decrypt(encrypted)
        res = Padding.unpad(res, AES.block_size)

        return res

    @staticmethod
    def decrypt_aes_cbc_src(encrypted, key, iv, bits=256):
        """使用 key 和 iv 原始字符解密"""
        key = AESCipher.mk_key(key, int(bits / 8))
        iv = AESCipher.mk_key(iv, AES.block_size)
        res = AES.new(key, AES.MODE_CBC, iv=iv).decrypt(encrypted)
        res = Padding.unpad(res, AES.block_size)

        return res

    @staticmethod
    def mk_bytes(data_src):
        """返回字节串"""
        return data_src if isinstance(data_src, bytes) else bytes(str(data_src), 'utf-8')

    @staticmethod
    def mk_pad_bytes(data_to_pad, length=AES.block_size):
        """字节串补齐"""
        return Padding.pad(AESCipher.mk_bytes(data_to_pad), length)

    @staticmethod
    def mk_key(key_src=None, length=16):
        """生成或补齐字节串"""
        if key_src is None:
            key = get_random_bytes(length)
        else:
            key = AESCipher.mk_pad_bytes(key_src, length)[:length]

        return key
