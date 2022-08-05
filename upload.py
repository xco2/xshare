from flask import Flask, request, render_template, session
from Serial import get_random_string
import cv2
import time, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


# 读取session
@app.route('/get')
def get():
    # session['username']
    # session.get('username')
    name = session.get('username')
    if name is None:
        return "None"
    else:
        return name


@app.route("/", methods=['GET', 'POST'])
def index():
    session['username'] = 'xco2'
    return "1"


@app.route("/upload", methods=["POST"])
def upload():
    """接受前端传送过来的文件"""
    file_obj = request.files.get("test_file")
    print(file_obj)
    if file_obj is None:
        return "文件上传为空"

    # 直接使用文件上传对象保存
    file_bytes = file_obj.read()

    with open("./demo.png", "wb") as f:
        f.write(file_bytes)

    return "文件上传成功"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=3000, debug=True)
