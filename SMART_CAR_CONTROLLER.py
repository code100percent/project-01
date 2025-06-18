from flask import Flask ,render_template,url_for,redirect
import socket
from time import sleep

app = Flask(__name__)
CarServerAddress = ("192.168.1.11",2222)
BufferSize = 1024
UDPClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

@app.route('/commands')
def index():
    return render_template('Smart_car_controller.html')

@app.route('/commands/<cmd>')
def send_cmd(cmd):
    
    print('cmd sending ... ',cmd)
    cmdEncoded = cmd.encode('utf-8')
    UDPClient.sendto(cmdEncoded,CarServerAddress)
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)