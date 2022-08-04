import time
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
from hashlib import md5


def bytes_to_key(data: str, output: int = 32) -> bytes:
    data = data.encode(encoding='utf-8')
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


# 加密
def encode(data: bytes, key: str, iv: str = None) -> bytes:
    key = bytes_to_key(key)
    if iv is None:
        iv = key[16:]
    else:
        iv = iv.encode('utf-8')
    key = key[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 加密
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    encrypted_data = base64.b64encode(encrypted_data)
    return encrypted_data


# 解密
def decode(encrypted_data: bytes, key: str, iv: str = None) -> bytes:
    key = bytes_to_key(key)
    if iv is None:
        iv = key[16:]
    else:
        iv = iv.encode('utf-8')
    key = key[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密
    encrypted_data = base64.b64decode(encrypted_data)
    data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return data


# 随机字符串
def get_random_string(size):
    import random, string

    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


class Serial:
    def __init__(self):
        # [序列号,随机数,]
        self.data = []
        self.creat_serial_key = "sgsrLFh2B28WGZvM"
        self.iv = "IP0vkIBiocoTjAeN"

    def get_serial(self, key):
        """

        :return:
        """
        t = str(int(time.time()))
        file_id = "{0:0>8}".format(np.random.randint(0, 99999999, 1)[0])  # 前4位作为文件id
        ser = t + file_id
        print(ser)
        en_ser = encode(ser.encode("utf-8"), self.creat_serial_key)
        en_ser = encode(en_ser, key)

        print("en", en_ser.decode("utf-8"))
        return en_ser.decode("utf-8")

    def use_serial(self, en_ser: str, key: str):
        en_ser = en_ser.encode("utf-8")
        data = decode(en_ser, key)
        data = decode(data, self.creat_serial_key)
        print("de", data)


if __name__ == '__main__':
    # print(get_random_string(16))
    s = Serial()
    for i in range(5):
        en_ser = s.get_serial("xco2")
        s.use_serial(en_ser, "xco2")
        print()
