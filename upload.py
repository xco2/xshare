from flask import Flask, request, render_template
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import cv2
import time

app = Flask(__name__)


def encode(data):
    # 随机生成16字节（即128位）的加密密钥
    key = "awdsasdfevasdveasdvasdvesdavsaew".encode('utf-8')
    print(key)
    iv = key[0:16]

    # 实例化加密套件，使用CBC模式
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 对内容进行加密，pad函数用于分组和填充
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    # 将加密内容写入文件
    with open("encrypted.bin", "wb") as file_out:
        # 在文件中依次写入key、iv和密文encrypted_data
        [file_out.write(x) for x in (key, cipher.iv, encrypted_data)]
    with open("./encode_demo.png", "wb") as f:
        f.write(encrypted_data)


def decode():
    # 从前边文件中读取出加密的内容
    with open("encrypted.bin", "rb") as file_in:
        # 依次读取key、iv和密文encrypted_data，16等是各变量长度，最后的-1则表示读取到文件末尾
        key, iv, encrypted_data = [file_in.read(x) for x in (32, AES.block_size, -1)]
    print(key)
    # 实例化加密套件
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密，如无意外data值为最先加密的b"123456"
    data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    # print(data.decode("utf-8"))
    with open("./decode_demo.png", "wb") as f:
        f.write(data)
    return data


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('test_upload.html')


@app.route("/upload", methods=["POST"])
def upload():
    """接受前端传送过来的文件"""
    file_obj = request.files.get("test_file")
    print(file_obj)
    if file_obj is None:
        return "文件上传为空"

    # 直接使用文件上传对象保存
    file_bytes = file_obj.read()
    encode(file_bytes)

    with open("./demo.png", "wb") as f:
        f.write(file_bytes)

    return "文件上传成功"


@app.route("/demo", methods=["GET"])
def demo():
    decode()
    return "1"

# 获取上传文件的序列号
@app.route("/getSerialNumber")
def get_upload_serial():
    pass

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=3000, debug=True)
