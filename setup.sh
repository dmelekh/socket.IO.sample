#!/bin/bash

# prerequisites
# pip3 install flask
# pip3 install flask-cors
# pip3 install flask-socketio

cd ~/socket.IO.sample/test_server
export FLASK_APP=run_server.py
python3 -m flask run

# address is in console log: http://0.0.0.0:8000/

