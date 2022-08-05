import random
import time
import numpy as np
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
from hashlib import md5


def time_it(f):
    def fun(*args, **kwargs):
        st = time.time()
        res = f(*args, **kwargs)
        print("fun:{0} {1:.4f}s".format(f.__name__, time.time() - st))
        return res

    return fun


# 通过不定长密码生成定长密码
def bytes_to_key(data: str, salt: bytes, output: int = 32) -> bytes:
    data = data.encode(encoding='utf-8')
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


# 加密
def encode(data: bytes, key: str) -> bytes:
    salt = Random.new().read(8)
    key = bytes_to_key(key, salt)
    iv = key[16:]
    key = key[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 加密
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    encrypted_data = base64.b64encode(b"Salted__" + salt + encrypted_data)
    return encrypted_data


# 解密
def decode(encrypted_data: bytes, key: str) -> bytes:
    encrypted_data = base64.b64decode(encrypted_data)
    assert encrypted_data[0:8] == b"Salted__"
    salt = encrypted_data[8:16]

    key = bytes_to_key(key, salt)
    iv = key[16:]
    key = key[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密
    data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
    return data


# 随机字符串
def get_random_string(size):
    import random, string

    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


class Serial:
    def __init__(self):
        self.users = ["xco2"]
        self.keys = ["qwer"]
        self.creat_serial_key = "MZ9pxk7Zy7gK7HGS"

    # 生成上传码,加密前,10位为时间,3位有效时间,5位文件id,加密后,最前面是授权者昵称
    def create_serial(self, key: str, v_t: int) -> [str, None]:
        """
        生成上传码,加密前,10位为时间,3位有效时间,5位文件id,加密后,最前面是授权者昵称
        :param key: 密码
        :param v_t: 有效时间,3位数,第一位为模式,0代表分钟为单位,1代表小时为单位,2代表天为单位,其余一律按秒算
        :return:
        """
        assert v_t > 0
        if key not in self.keys:
            # 如果没有记录这个密码证明没有权限,随机生成一个用户名,反正也解不出来
            user = get_random_string(random.randint(3, 67))
        else:
            user = self.users[self.keys.index(key)]

        t = str(int(time.time()))
        v_t = "{0:0>3}".format(v_t)
        file_id = "{0:0>5}".format(np.random.randint(0, 99999, 1)[0])
        ser = t + v_t + file_id
        print(ser)

        # 加密
        en_ser = encode(ser.encode("utf-8"), self.creat_serial_key)
        en_ser = encode(en_ser, key)
        en_ser = "{0:->6}".format(user) + "_" + en_ser.decode("utf-8")

        print("en", en_ser)
        return en_ser

    # 验证上传码
    def check_serial(self, en_ser: str) -> [int, None]:
        """
        验证上传码
        :param en_ser:上传码
        :return: 不存在返回None
                 超时返回-1
                 合法返回文件id
        """
        user, en_ser = en_ser.split("_")
        user = user.split("-")[-1]
        if user not in self.users:
            return None
        key = self.keys[self.users.index(user)]

        # 解密
        en_ser = en_ser.encode("utf-8")
        data = decode(en_ser, key)
        data = decode(data, self.creat_serial_key)
        data = data.decode("utf-8")

        # 切割
        t = int(data[:10])
        v_t = data[10:13]  # 有效时间,3位数,第一位为模式,0代表分钟为单位,1代表小时为单位,2代表天为单位,其余一律按秒算
        if v_t[0] == 0:  # 分钟
            v_t = int(v_t[1:]) * 60
        elif v_t[0] == 1:  # 小时
            v_t = int(v_t[1:]) * 3600
        elif v_t[0] == 2:  # 天
            v_t = int(v_t[1:]) * 3600 * 24
        else:  # 其余一律按秒算
            v_t = int(v_t[1:])
        file_id = int(data[13:])
        print("de", data)
        # 判断是否超时
        if time.time() > t + v_t:
            return -1
        else:
            return file_id

    # 验证通过后,把文件id与授权者的映射存入数据库,保存的文件由文件id+时间戳命名,
    # 文件保存一段时间后删除,若没有已文件id开头的文件了,就删除数据库中的映射


if __name__ == '__main__':
    s = Serial()
    for i in range(3):
        en_ser = s.create_serial("qwer", 2)
        print(len(en_ser), en_ser)
        time.sleep(2)
        file_id = s.check_serial(en_ser)
        print("file_id", file_id)
        print()
