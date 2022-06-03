from flask_socketio import emit, Namespace
from __main__ import socketio

class Socket(Namespace):
    #events
    @socketio.on_error()        # Handles the default namespace
    def error_handler(e):
        print(e)
    # API ENDPOINTS
    @socketio.on('connect')
    def initial_connection():
        print('A new client connect')

    @socketio.on("F2B_btn_click")
    def button():
        print("test")


    #emits
    def emit_distance(value):
        socketio.emit('B2F_send_distance', {'distance': value})