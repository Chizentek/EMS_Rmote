from __future__ import unicode_literals
import os
import sys

from flask import Flask, request, abort, render_template, url_for, flash, redirect, send_file, copy_current_request_context
from flask import render_template_string, stream_with_context
#from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import configparser

from flask_socketio import SocketIO, emit
from random import random
# from time import sleep
import webbrowser
from threading import Thread, Event, Timer
# from multiprocessing.pool import ThreadPool
# import subprocess

import math
import timeit
import time
from engineio.async_drivers import eventlet
# https://github.com/miguelgrinberg/python-socketio/issues/35
# Add the following two lines at file head, it's useless to the python file, but it's necessary for pyinstaller packing. (may not!!)
from eventlet.hubs import epolls, kqueue, selects
from dns import dnssec, e164, hash, namedict, tsigkeyring, update, version, zone

# from flask_images import resized_img_src

testmode = 1
COM_PORT = None
UUID = None
stop_flag = 1


# === Global Var ====
en_temp = None
on_off = None
mode = None
ac_temp = None
fan = None


#  取得啟動文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))
print("pjdir=", pjdir)
# print(os.getcwd())
# print(os.path.join(pjdir, 'static', 'img', 'schoolbg.png'))

# config 初始化
config = configparser.ConfigParser()
config.read('config.ini')

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    hex_folder = os.path.join(sys._MEIPASS, 'hex')
    app = Flask(__name__, template_folder=template_folder,
                static_folder=static_folder)
else:
    app = Flask(__name__)


def open_browser():

    paths = [r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
             r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"]

    # 檢查檔案是否存在
    for filepath in paths:
        if os.path.isfile(filepath):
            print("Chrome存在")
            chrome = webbrowser.get(
                r"{} --app=%s".format(filepath))  # --start-fullscreen --ignore-certificate-errors
            chrome.open('http://localhost:5000/test.html')
        else:
            print("Chrome不存在")


# ----------------------------------------------------------------------------------------------
# turn the flask app into a socketio app
#　https://stackoverflow.com/questions/47875007/flask-socket-io-frequent-time-outs
socketio = SocketIO(app, async_mode='eventlet', logger=True, engineio_logger=True, ping_interval=10000,
                    ping_timeout=5000)  # ping_interval = 10000, ping_timeout = 5000 for delay the timeout
# socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()
# isClosed = True


# -----------------------------------------------------------------------


@app.route('/test.html')
def test():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('test.html')

# -------------------------------------------------------------------------------------------------


@socketio.on('connect', namespace='/test')
def test_connect():

    global thread
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.is_alive():
        print("Starting Thread")
        #thread = socketio.start_background_task(randomNumberGenerator)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

# -------------------------------------------------------------------------------------------------


def test_data():
    global en_temp
    global on_off
    global mode
    global ac_temp
    global fan

    en_temp = 28
    on_off = "on"
    mode = "auto"
    ac_temp = 25
    fan = "High"

    socketio.emit(
        'data', {'en_temp': en_temp, 'on_off': on_off, 'mode': mode, 'ac_temp': ac_temp, 'fan': fan}, namespace='/test')


@socketio.on('start_data')
def handle_start_data():
    print('start sending data')
    global stop_flag
    stop_flag = 0
    test_data()


# =================================================================================================


if __name__ == '__main__':
    Timer(1, open_browser).start()

    app.debug = False
    socketio.run(app, host='127.0.0.1', port=5000)
    # app.run( host='127.0.0.1', port = 5000, ssl_context=('server.crt', 'server.key'))
    # socketio.run(app, host='127.0.0.1', port = 5000, keyfile='server.key', certfile='server.crt')
