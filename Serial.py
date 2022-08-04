import time
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


# 加密
def encode(data: bytes, key: str, iv: str) -> bytes:
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 加密
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    encrypted_data = base64.b64encode(encrypted_data)
    return encrypted_data


# 解密
def decode(encrypted_data: bytes, key: str, iv=str) -> bytes:
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
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
        生成一个上传文件所需要的序列号,该序列号与文件一同上传,序列号中包含时间,用于判断序列号是否过期,
        :return:
        """
        t = str(int(time.time()))
        ran = "{0:0>5}".format(np.random.randint(0, 99999, 1)[0])
        ser = t + ran
        en_ser = encode(ser.encode("utf-8"), self.creat_serial_key, self.iv)
        en_ser = encode(en_ser, key, self.iv)

        print(en_ser.decode("utf-8"))
        return en_ser.decode("utf-8")

    def use_serial(self):
        pass

if __name__ == '__main__':
    # print(get_random_string(16))
    s = Serial()
    for i in range(5):
        s.get_serial("xco2")
