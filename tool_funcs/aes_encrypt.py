# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import base64


class AesEncryptor(object):
    
    def __init__(self):
        self.secret_key = "sqlKey"
        self.iv_key = "sqlIv"
        self.block_size = 16
    
    def get_iv_key_bytes(self, iv_key):
        iv_bytes = iv_key.encode(encoding='utf-8')
        iv_key_bytes = []
        if len(iv_bytes) >= self.block_size:
            iv_key_bytes = iv_bytes[:self.block_size]
        else:
            iv_key_bytes.extend(iv_bytes)
            iv_key_bytes.extend([0 for x in range(0, self.block_size - len(iv_bytes))])
        return iv_key_bytes
    
    def init_cipher(self):
        secret_bytes = self.secret_key.encode(encoding='utf-8')
        key_bytes = []
        if len(secret_bytes) >= self.block_size:
            key_bytes = secret_bytes[:self.block_size]
        else:
            key_bytes.extend(secret_bytes)
            key_bytes.extend([0 for x in range(0, self.block_size - len(secret_bytes))])
    
        iv_key_bytes = self.get_iv_key_bytes(self.iv_key)
        cipher = AES.new(bytes(key_bytes), AES.MODE_CBC, bytes(iv_key_bytes))
        return cipher
    
    def init_cipher_bytes(self, iv_key_bytes):
        secret_bytes = self.secret_key.encode(encoding='utf-8')
        key_bytes = []
        if len(secret_bytes) >= self.block_size:
            key_bytes = secret_bytes[:self.block_size]
        else:
            key_bytes.extend(secret_bytes)
            key_bytes.extend([0 for x in range(0, self.block_size - len(secret_bytes))])
        cipher = AES.new(bytes(key_bytes), AES.MODE_CBC, bytes(iv_key_bytes))
        return cipher
    
    def aes_encrypt(self, value):
        cipher = self.init_cipher()
        buffer = value.encode(encoding="utf-8")
        bufferList = list(buffer)
        # 数据进行 PKCS5Padding 的填充
        padding = self.block_size - len(bufferList) % self.block_size
        bufferList.extend([padding for x in range(0, padding)])
        iv_key_bytes = self.get_iv_key_bytes(self.iv_key)
        iv_64 = base64.b64encode(bytes(iv_key_bytes))
        buffer = cipher.encrypt(bytes(bufferList))
        return str(iv_64, encoding='utf-8') + ";" + buffer.hex()  # 使用hex格式输出
    
    def aes_decrypt(self, value):
        encrypt_fields = value.split(';')
        iv_64 = encrypt_fields[0]
        iv_key_bytes = base64.b64decode(iv_64)
        value = encrypt_fields[1]
        cipher = self.init_cipher_bytes(iv_key_bytes)
        buffer = bytes.fromhex(value)  # 读取hex格式数据
        buffer = cipher.decrypt(buffer)
        result = buffer.decode("utf-8")
        # 去掉 PKCS5Padding 的填充
        return result[:-ord(result[len(result) - 1:])]