import numpy as np
from flask import Flask, request, render_template, session, jsonify, Response, make_response
from flask_apscheduler import APScheduler
from Serial import Serial, encode, decode
import cv2
import time, os, json
from PIL import Image
from loguru import logger
from flask_cors import CORS
from calibrate_camera import *
import datetime

# 43.138.187.142
server_ip = "0.0.0.0"
port = 13000
upload_files_save_path = "./uploadFiles"
upload_encrypted_files_save_path = "./encryptedFiles"

upload_calibrate_camera_save_path = "./calib_camera_imgs"

# flask
app = Flask(__name__, static_folder=upload_files_save_path)
app.config['SECRET_KEY'] = os.urandom(24)
# app.config['SESSION_PERMANENT'] = True  # 如果设置为True，则关闭浏览器session就失效。
# app.permanent_session_lifetime = datetime.timedelta(seconds=600)  # 设置session过期时间
CORS(app, resources={r"/*": {"origins": "*"}})  # 跨域

# 定时任务
scheduler = APScheduler()

# 加解密模块
serial_home = Serial()


# 没试过不知道能不能解决
# @app.after_request
# def af_req(resp):  # 解决跨域session丢失
#     resp = make_response(resp)
#     resp.headers['Access-Control-Allow-Origin'] = f'http://{server_ip}:{port}'
#     resp.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,OPTIONS'
#     # resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#     resp.headers[
#         'Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild'
#     resp.headers['Access-Control-Allow-Credentials'] = 'true'
#
#     # resp.headers['X-Powered-By'] = '3.2.1'
#     # resp.headers['Content-Type'] = 'application/json;charset=utf-8'
#     return resp


# =======================定时清理=======================
@scheduler.task('cron', id='clean_files', day='*', hour='4', minute='00', second='00')
def clean_files_schedul():
    return clean_files()


# 多套一层方便手动调用
def clean_files():
    now_time = time.time()

    # 无加密文件,加密文件
    for save_path in [upload_files_save_path, upload_encrypted_files_save_path]:
        for root, dirs, files in os.walk(save_path):
            for f in files:
                f_time = int(f.split("_")[1].split("@")[0])
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
        try:
            json_data = request.json
        except:
            json_data = None
        if json_data is not None:  # json方式
            is_json = True
            logger.info(json_data)
            key = json_data["key"]  # 密码
            try:
                v_t = int(json_data["v_t"])  # 有效时间
            except:
                v_t = None
        else:  # form表单方式
            is_json = False
            key = request.form.get("key")
            try:
                v_t = int(request.form["v_t"])  # 有效时间
            except:
                v_t = None

        if v_t is None:
            return jsonify({"code": -1, "msg": "有效时间错误", "data": None})

        serial, file_id = serial_home.create_serial(key, v_t)
        session['file_id'] = file_id
        if is_json:
            return jsonify({"code": 1, "msg": "", "data": serial})
        else:
            return serial
    else:
        return jsonify({"code": -1, "msg": "请求错误", "data": None})
        # return "-1"


# 检测上传码
@app.route("/checkSerial", methods=['POST'])
def check_serial():
    global serial_home
    if request.method == 'POST':
        try:
            json_data = request.json
        except:
            json_data = None
        if json_data is not None:
            is_json = True
            logger.info(json_data)
            serial = json_data["serial"]
        else:
            is_json = False
            serial = request.form['serial']
        if serial is None:
            # return "错误上传码,<a href='/'>返回</a>"
            return jsonify({"code": -1, "msg": "错误上传码", "expires": "", "data": False})

        file_id, user, expires = serial_home.check_serial(serial)
        logger.info(file_id)

        if file_id is None:
            if is_json:
                return jsonify({"code": -1, "msg": "错误上传码", "expires": "-1", "data": False})
            else:
                return "错误上传码,<a href='/'>返回</a>"
        elif file_id == -1:
            if is_json:
                return jsonify({"code": -1, "msg": "上传码已过期", "expires": "-1", "data": False})
            else:
                return "上传码已过期,<a href='/'>返回</a>"
        else:
            # session['file_id'] = file_id
            if is_json:
                return jsonify({"code": 1, "msg": "通过验证", "expires": expires, "data": True})
            else:
                return "<script>window.location = '/'</script>"
    else:
        return jsonify({"code": -1, "msg": "错误上传码", "expires": "-1", "data": False})
        # return "错误上传码,<a href='/'>返回</a>"


# =======================上传文件======================
# 生成压缩图
def create_litter_img(img_path: str, shape=100):
    img = Image.open(img_path)
    w, h = img.size
    wph = w / h
    if w > h:
        w = shape
        h = int(w / wph)
    else:
        h = shape
        w = int(wph * h)
    img = img.resize((w, h))
    img_name = os.path.split(img_path)[-1]
    img_dir = img_path.replace(img_name, "")
    img.save(os.path.join(img_dir, "s" + img_name))


# 上传文件,无加密
@app.route("/upload", methods=["POST"])
def upload():
    """
    接受前端传送过来的文件,不需要加密
    :return:
    """
    global upload_files_save_path, serial_home
    authorization = request.headers.get('XAuthorization')
    # print(authorization, type(authorization))
    if authorization is None:
        return jsonify({"code": -1, "msg": "无授权", "data": False})
        # return "未输入上传码,<a href='/'>返回</a>"
    else:
        file_id, user, expires = serial_home.check_serial(str(authorization))
        logger.info(file_id)
        if file_id is None:
            return jsonify({"code": -1, "msg": "无授权", "data": False})
        elif file_id == -1:
            return jsonify({"code": -1, "msg": "授权过期", "data": False})
        else:
            # 获取上传的文件
            file_objs = request.files.getlist("upload_file")
            if file_objs is None:
                return jsonify({"code": -1, "msg": "文件上传为空", "data": False})
                # return "文件上传为空,<a href='/'>返回</a>"
            for file_obj in file_objs:
                file_bytes = file_obj.read()
                logger.info("文件大小{0}M".format(len(file_bytes) / 8 / 1024 / 1024))
                if len(file_bytes) > 1024 * 1024 * 1024 * 8:  # 文件大小限制,1G
                    return jsonify({"code": -1, "msg": "文件过于100MB", "data": False})
                # return "文件过于100MB,<a href='/'>返回</a>"

                file_type = file_obj.filename.split(".")[-1]
                file_name = str(file_id) + "_" + str(int(time.time())) + "@" + file_obj.filename
                file_name = os.path.join(upload_files_save_path, file_name)
                with open(file_name, "wb") as f:
                    f.write(file_bytes)
                if file_type in ["png", "jpg", "jpeg"]:
                    create_litter_img(file_name)
            # return "文件上传成功{0},<a href='/'>返回</a>".format(file_id)
            return jsonify({"code": 1, "msg": "文件上传成功{0}".format(file_id), "data": True})


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
            if f[0] == "s":
                continue
            f_type = f.split(".")[-1]
            if f_type in ["png", "jpg", "jpeg"]:
                res += "<a href='/{0}/{1}'><img src='/{0}/s{1}'></a><br>".format(
                    upload_files_save_path.split("/")[-1], f)
            else:
                res += "<a href='/{0}/{1}'>{1}</a><br>".format(upload_files_save_path.split("/")[-1], f)
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


# =====================获取摄像机内参===================

@app.route("/calibrateCamera", methods=["POST"])
def calibrate_camera():
    uploaded_dir = upload_chessboard_img(upload_calibrate_camera_save_path)
    if uploaded_dir:
        imgs = load_imgs(uploaded_dir)
        try:
            k_cam, dist_coeffs, _, _ = calib_camera(imgs)
            k_cam = str(k_cam)
            dist_coeffs = str(dist_coeffs)
            return jsonify({"code": 1, "msg": "成功获取内参数", "data": [k_cam, dist_coeffs]})
        except:
            return jsonify({"code": -1, "msg": "获取内参数失败", "data": False})
    else:
        return jsonify({"code": -1, "msg": "照片数量不足", "data": False})


# ======================视频流=========================
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    yield b'--frame\r\n'
    index = 0
    while True:
        frame = open("video_imgs/" + str(index) + '.png', 'rb').read()
        time.sleep(0.2)
        index = (index + 1) % 300
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


if __name__ == '__main__':
    # 上传分享文件的目录
    if not os.path.exists(upload_files_save_path):
        os.mkdir(upload_files_save_path)
    if not os.path.exists(upload_encrypted_files_save_path):
        os.mkdir(upload_encrypted_files_save_path)

    # 上传矫正摄像机照片的目录
    if not os.path.exists(upload_calibrate_camera_save_path):
        os.mkdir(upload_calibrate_camera_save_path)

    clean_files()

    scheduler.init_app(app)
    scheduler.start()
    app.run(host=server_ip, port=port, debug=False)
