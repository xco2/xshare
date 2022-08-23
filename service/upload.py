from flask import Flask, request, render_template, session, jsonify, Response
from flask_apscheduler import APScheduler
from Serial import Serial, encode, decode
import cv2
import time, os, json
from loguru import logger

# 43.138.187.142
server_ip = "0.0.0.0"
port = 13000
upload_files_save_path = "./uploadFiles"
upload_encrypted_files_save_path = "./encryptedFiles"

# flask
app = Flask(__name__, static_folder=upload_files_save_path)
app.config['SECRET_KEY'] = os.urandom(24)

# 定时任务
scheduler = APScheduler()

# 加解密模块
serial_home = Serial()


@scheduler.task('cron', id='clean_files', day='*', hour='4', minute='00', second='00')
def clean_files():
    now_time = time.time()

    # 无加密文件,加密文件
    for save_path in [upload_files_save_path, upload_encrypted_files_save_path]:
        for root, dirs, files in os.walk(save_path):
            for f in files:
                f_time = int(f.split("_")[1].split(".")[0])
                # 超过3天删除
                if now_time - f_time >= 3 * 24 * 60 * 60:
                    file_path = os.path.join(save_path, f)
                    os.remove(file_path)
                    logger.info("删除{0}".format(file_path))


# =======================上传码======================

@app.route("/", methods=['GET', 'POST'])
def index():
    # session['username'] = 'xco2'
    # session['username']
    # session.get('username')
    # name = session.get('username')
    return render_template('upload.html')


# 获取上传码
@app.route("/createSerial", methods=['POST'])
def serial_creater():
    global serial_home
    if request.method == 'POST':
        # json_data = request.json
        # json_data = json.loads(json_data)
        # logger.info(json_data)
        # key = json_data["key"]  # 密码
        key = request.form["key"]
        try:
            # v_t = int(json_data["v_t"])  # 有效时间
            v_t = int(request.form["v_t"])  # 有效时间
        except:
            # return jsonify({"code": -1, "msg": "有效时间错误"})
            return "有效时间错误"

        serial, file_id = serial_home.create_serial(key, v_t)
        session['file_id'] = file_id
        # return jsonify({"code": 1, "serial": serial})
        return serial
    else:
        # return jsonify({"code": -1})
        return "-1"


# 检测上传码
@app.route("/checkSerial", methods=['POST'])
def check_serial():
    global serial_home
    if request.method == 'POST':
        # json_data = request.json
        # json_data = json.loads(json_data)
        # logger.info(json_data)
        # serial = json_data["serial"]
        serial = request.form['serial']
        file_id, user = serial_home.check_serial(serial)
        logger.info(file_id)
        if file_id is None:
            # return jsonify({"code": -1, "msg": "错误上传码"})
            return "错误上传码,<a href='/'>返回</a>"
        elif file_id == -1:
            # return jsonify({"code": 0, "msg": "上传码已过期"})
            return "上传码已过期,<a href='/'>返回</a>"
        else:
            # TODO: 添加授权者与file_id的映射到数据库
            session['file_id'] = file_id
            # return jsonify({"code": 1, "msg": "通过验证"})
            return "通过验证,<a href='/'>返回</a>"
    else:
        # return jsonify({"code": -1, "msg": "错误上传码"})
        return "错误上传码,<a href='/'>返回</a>"


# =======================上传文件======================

# 上传文件,无加密
@app.route("/upload", methods=["POST"])
def upload():
    """
    接受前端传送过来的文件,不需要加密
    :return:
    """
    global upload_files_save_path
    file_id = session.get('file_id')
    logger.info(file_id)
    if file_id is None:
        # return jsonify({"code": -1, "msg": "未输入上传码"})
        return "未输入上传码,<a href='/'>返回</a>"
    else:
        # 获取上传的文件
        file_obj = request.files.get("upload_file")
        if file_obj is None:
            # return jsonify({"code": -1, "msg": "文件上传为空"})
            return "文件上传为空,<a href='/'>返回</a>"

        file_bytes = file_obj.read()
        logger.info("文件大小{0}KB".format(len(file_bytes) / 8 / 1024))
        if len(file_bytes) > 100 * 1024 * 1024 * 8:  # 文件大小限制,100MB
            # return jsonify({"code": -1, "msg": "文件过于100MB"})
            return "文件过于100MB,<a href='/'>返回</a>"

        file_type = file_obj.filename.split(".")[-1]
        file_name = str(file_id) + "_" + str(int(time.time())) + "." + file_type
        with open(os.path.join(upload_files_save_path, file_name), "wb") as f:
            f.write(file_bytes)

        return "文件上传成功{0},<a href='/'>返回</a>".format(file_id)


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
        file_name = str(file_id) + "_" + str(int(time.time())) + "." + file_type
        with open(os.path.join(upload_encrypted_files_save_path, file_name), "wb") as f:
            f.write(file_bytes)

        return jsonify({"code": 1, "msg": "文件上传成功"})


# ======================获取文件列表======================

# 获取文件列表
@app.route("/files", methods=["GET", "POST"])
def get_files():
    res = ""
    for root, dirs, files in os.walk(upload_files_save_path):
        for f in files:
            f_type = f.split(".")[-1]
            if f_type in ["png", "jpg", "jpeg"]:
                res += "<a href='/{0}/{1}'><img src='/{0}/{1}' height='200'></a><br>".format(
                    upload_files_save_path.split("/")[-1], f)
            else:
                res += "<a href='/{0}/{1}'>{1}</a><br>".format(upload_files_save_path.split("/")[-1], f)
    print(res)
    return res + "<br><a href='/'>返回</a>"


# 获取加密文件列表
@app.route("/filesEncrypted", methods=["GET", "POST"])
def get_encrypted_files():
    files = ""
    for root, dirs, files in os.walk(upload_files_save_path):
        files.append(
            """<form action='/decrypt' method='post'>
            <input type='text' name='file' value='{0}'>
            <input type='text' name='key'>
            <input type='submit'>
            </form>\n""".format(files))

    return files


# =======================解密文件=====================
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

    scheduler.init_app(app)
    scheduler.start()
    app.run(host=server_ip, port=port, debug=False)
