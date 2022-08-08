from flask import Flask, request, render_template, session, jsonify, Response
from Serial import Serial, encode, decode
import cv2
import time, os, json
from loguru import logger

server_ip_port = "127.0.0.1:3000"
upload_files_save_path = "./uploadFiles"
upload_encrypted_files_save_path = "./encryptedFiles"

app = Flask(__name__, static_folder=upload_files_save_path)
app.config['SECRET_KEY'] = os.urandom(24)
serial_home = Serial()


@app.route("/", methods=['GET', 'POST'])
def index():
    # session['username'] = 'xco2'
    # session['username']
    # session.get('username')
    # name = session.get('username')
    render_template('upload.html')


# 获取上传码
@app.route("/createSerial", methods=['POST'])
def serial_creater():
    global serial_home
    if request.method == 'POST':
        json_data = request.json
        json_data = json.loads(json_data)
        logger.info(json_data)
        key = json_data["key"]  # 密码
        v_t = json_data["v_t"]  # 有效时间

        serial = serial_home.create_serial(key, v_t)
        return jsonify({"code": 1, "serial": serial})
    else:
        return jsonify({"code": -1})


# 检测上传码
@app.route("/checkSerial", methods=['POST'])
def check_serial():
    global serial_home
    if request.method == 'POST':
        json_data = request.json
        json_data = json.loads(json_data)
        logger.info(json_data)
        serial = json_data["serial"]
        file_id = serial_home.check_serial(serial)
        if file_id is None:
            return jsonify({"code": -1, "msg": "错误上传码"})
        elif file_id == -1:
            return jsonify({"code": 0, "msg": "上传码已过期"})
        else:
            # TODO: 添加授权者与file_id的映射到数据库
            session['file_id'] = file_id
            return jsonify({"code": 1, "msg": "通过验证"})
    else:
        return jsonify({"code": -1, "msg": "错误上传码"})


# ====================================================

# 上传文件,无加密
@app.route("/upload", methods=["POST"])
def upload():
    """
    接受前端传送过来的文件,不需要加密
    :return:
    """
    global upload_files_save_path
    file_id = session.get('username')
    if file_id is None:
        return jsonify({"code": -1, "msg": "未输入上传码"})
    else:
        # 获取上传的文件
        file_obj = request.files.get("test_file")
        if file_obj is None:
            return jsonify({"code": -1, "msg": "文件上传为空"})

        file_bytes = file_obj.read()
        logger.info("文件大小{0}KB".format(len(file_bytes) / 8 / 1024))
        if len(file_bytes) > 100 * 1024 * 1024 * 8:  # 文件大小限制,100MB
            return jsonify({"code": -1, "msg": "文件过于100MB"})

        file_type = file_obj.filename.split(".")[-1]
        file_name = str(file_id) + "_" + str(time.time()) + "." + file_type
        with open(os.path.join(upload_files_save_path, file_name), "wb") as f:
            f.write(file_bytes)

        return jsonify({"code": 1, "msg": "文件上传成功"})


# 上传文件,加密
@app.route("/uploadEncrypt", methods=["POST"])
def upload_encrypt():
    """
    接受前端传送过来的文件,加密
    :return:
    """
    global upload_files_save_path
    file_id = session.get('username')
    if file_id is None:
        return jsonify({"code": -1, "msg": "未输入上传码"})
    else:
        # 获取上传的文件
        file_obj = request.files.get("test_file")
        if file_obj is None:
            return jsonify({"code": -1, "msg": "文件上传为空"})

        file_bytes = file_obj.read()
        logger.info("文件大小{0}KB".format(len(file_bytes) / 8 / 1024))
        if len(file_bytes) > 30 * 1024 * 1024 * 8:  # 文件大小限制,30MB
            return jsonify({"code": -1, "msg": "文件过于30MB"})

        # 加密
        key = request.form.get("key")
        file_bytes = encode(file_bytes, key)

        file_type = file_obj.filename.split(".")[-1]
        file_name = str(file_id) + "_" + str(time.time()) + "." + file_type
        with open(os.path.join(upload_encrypted_files_save_path, file_name), "wb") as f:
            f.write(file_bytes)

        return jsonify({"code": 1, "msg": "文件上传成功"})


# ====================================================

# 获取文件列表
@app.route("/files", methods=["GET", "POST"])
def getfiles():
    files = ""
    for root, dirs, files in os.walk(upload_files_save_path):
        files.append("<a href='{0}'>{0}</a>\n".format(files))

    return files


# 获取加密文件列表
@app.route("/filesEncrypted", methods=["GET", "POST"])
def getfiles():
    files = ""
    for root, dirs, files in os.walk(upload_files_save_path):
        files.append(
            """<form action='/decrypt' method='post'>
            <input type='text' name='file' value='{0}'>
            <input type='text' name='key'>
            <input type='submit'>
            </form>\n""".format(files))

    return files


# ====================================================
# 解密文件
@app.route("/decrypt", methods=["POST"])
def decrypt_file():
    file = request.form.get("file")
    key = request.form.get("key")

    with open(os.path.join(upload_encrypted_files_save_path, file), "rb") as f:
        file_bytes = f.read()
        try:
            file_bytes = decode(file_bytes, key)
        except:
            return jsonify({"code": -1, "msg": "密码有误"})

        return Response(file_bytes)


if __name__ == '__main__':
    if not os.path.exists(upload_files_save_path):
        os.mkdir(upload_files_save_path)
    if not os.path.exists(upload_encrypted_files_save_path):
        os.mkdir(upload_encrypted_files_save_path)
    app.run(host="127.0.0.1", port=3000, debug=True)
