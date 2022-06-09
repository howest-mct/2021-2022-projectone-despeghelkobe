from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify




class Socket:
    
    


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
    def emit_distance(self, value):
        self.socketio.emit('B2F_send_distance', {'distance': value})
    
    def emit_wallCrash(self):
        self.socketio.emit('B2F_wall_crash')