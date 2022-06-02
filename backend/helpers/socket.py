from flask_socketio import SocketIO, emit, Namespace
# try:
#     from __main__ import socketio, test_socket 
# except ImportError:
#     from app import socketio, test_socket
from __main__ import socketio

class Socket(Namespace):
    @socketio.on("F2B_btn_click")
    def button():
        print("test")