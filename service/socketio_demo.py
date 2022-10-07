from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(cors_allowed_origins='*')
socketio.init_app(app)

name_space = '/echo'


@app.route('/')
def index():
    return "123"


@app.route('/push')
def push_once():
    event_name = 'testemit'
    broadcasted_data = {'data': "test message!"}
    # 设置广播数据
    socketio.emit(event_name, broadcasted_data, namespace=name_space)
    return 'done!'


@socketio.on('connect', namespace=name_space)
def connected_msg():
    print('client connected.')


@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    print('client disconnected.')


# @socketio.on('my_event', namespace=name_space)
def mtest_message(message):
    print(message)
    emit('my_response', {'data': message['data'], 'count': 1})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=13000, debug=True)
