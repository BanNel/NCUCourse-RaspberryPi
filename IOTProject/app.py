# import required modules
from flask import Flask, render_template, Response 
# import picamera 
# import cv2
# import socket 
# import io 

#import tkinterButton
app = Flask(__name__) 

@app.route('/') 
def main():
    return render_template('index.html')

@app.route('/ShowImage')
def main1():
    return render_template('index.html')

@app.route('/CloseImage')
def main2():
    return render_template('index.html')

#####處理path路徑
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)
    
if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True, threaded=True) 