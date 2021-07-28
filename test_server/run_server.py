
from flask import Flask
from flask import render_template

import json
import os
from os import path
import shutil

from flask_socketio import SocketIO
from flask_socketio import emit


app = Flask(__name__)

app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    emit('on connect', {'data': 'Connected'})

@socketio.on('json')
def handle_my_custom_event(data):
    parsed = json.loads(data)
    if parsed['event-name'] != 'test':
        emit("on '" + parsed['event-name'] + "' server reaction", parsed['message'] + ' processed by server')

@socketio.on('test')
def handle_my_test_event(data):
    emit("server test handler reaction", data + ' processed by server test handler')


class TestFrontDirs:
    
    def __init__(self):
        self.front_dirs = ['static', 'templates']
        self.test_server_dir = path.dirname(__file__)
        self.proj_dir = path.dirname(self.test_server_dir)
        self.__replace_front_dirs()

    def __del__(self):
        self.__del_front_dirs()
        self.__del_pycache()
        
    def update(self):
        self.__replace_front_dirs()

    def __del_front_dirs(self):
        for basicname in self.front_dirs:
            self.__remove(basicname)
    
    def __del_pycache(self):
        self.__remove('__pycache__')

    def __replace_front_dirs(self):
        for basicname in self.front_dirs:
            print(basicname)
            self.__remove(basicname)
            self.__copy(basicname)
            
    def __remove(self, dir_basicname):
        test_front_dir = path.join(self.test_server_dir, dir_basicname)
        if (path.isdir(test_front_dir)):
            shutil.rmtree(test_front_dir)
    
    def __copy(self, dir_basicname):
        test_front_dir = path.join(self.test_server_dir, dir_basicname)
        proj_front_dir = path.join(self.proj_dir, dir_basicname)
        shutil.copytree(proj_front_dir, test_front_dir)
        self.__correctHtml(dir_basicname)
    
    def __correctHtml(self, dir_basicname):
        for root, dirs, files in os.walk(dir_basicname):
            for file in files:
                if (path.splitext(file)[1] == '.html'):
                    html_full_filename = path.join(self.test_server_dir, path.join(root, file))
                    lines = None
                    with open(html_full_filename) as f:
                        lines = f.readlines()
                        for i in range(len(lines)):
                            if ('path=' in lines[i]):
                                lines[i] = lines[i].replace('path=', 'filename=')
                    if (lines != None):
                        with open(html_full_filename, 'w') as f:
                            f.writelines(lines)

testFrontDirs = TestFrontDirs()

@app.route('/')
def index():
    print('index()')
    testFrontDirs.update()
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
