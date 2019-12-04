# import required modules

from flask import Flask,jsonify,  render_template, Response 
# import picamera 
# import cv2
# import socket 
# import io
import requests
from io import BytesIO
from PIL import Image, ImageTk
from threading import Thread

from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
import threading
import argparse
import datetime
import imutils
import time
import cv2
import operator

import showImage
#import tkinterButton

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
# Import 人臉訓練集 Model(找尋人臉定位)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# 宣告基本參數
cascade_scale = 1.2
cascade_neighbors = 6
minFaceSize = (30,30)
vs = VideoStream(src=0).start()
time.sleep(2.0)
emotion_label = "None"

app = Flask(__name__) 

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock

    # initialize the motion detector and the total number of frames
    # read thus far
    #md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    # Import Trained Model
    model_path = "emotions-recognition-retail-0003.xml"
    pbtxt_path = "emotions-recognition-retail-0003.bin"
    net = cv2.dnn.readNet(model_path, pbtxt_path)
    
    # Specify target device
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # Read an image
        out = []
        frame_c = frame.copy()

        # Call getFaces() 找找臉在哪裡，給予臉部定位
        faces = getFaces(frame_c)
        x, y, w, h = 0, 0, 0, 0
        i = 0
        
        for (x,y,w,h) in faces:
            # 臉部的框框
            # cv2.rectangle(影像, 頂點座標, 對向頂點座標, 顏色, 線條寬度)
            cv2.rectangle( frame_c,(x,y),(x+w,y+h),(0,0,255),2)
        
            if(w>0 and h>0):
                    facearea = frame_c[y:y+h, x:x+w]

                    # Prepare input blob and perform an inference
                    blob = cv2.dnn.blobFromImage(facearea, size=(64, 64), ddepth=cv2.CV_8U)

                    # 辨識表情 (輸入臉部)
                    net.setInput(blob)

                    # 辨識表情 (return 機率)
                    out = net.forward()
                    neutral = int(out[0][0][0][0] * 100)
                    happy = int(out[0][1][0][0] * 100)
                    sad = int(out[0][2][0][0] * 100)
                    surprise = int(out[0][3][0][0] * 100)
                    anger = int(out[0][4][0][0] * 100)
                    yy = y
                    
                    # 印出最高機率的表情 (我寫的)
                    stats = {'neutral':neutral, 'happy':happy, 'sad': sad, 'surprise': surprise, 'anger': anger}    
                    emot = max(stats.items(), key=operator.itemgetter(1))[0]
                    print (emot)
                    global emotion_label
                    emotion_label = emot

#                    # 印出來(所有機率、其他文字)
#                    line2 = "{}%\n{}%\n{}%\n{}%\n{}%".format(neutral,happy,sad,surprise,anger)
#                    y0, dy = yy, 35
#                    for ii, txt in enumerate(line2.split('\n')):
#                        y = y0 + ii*dy
#                        cv2.putText(frame_c, txt, (x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#
#                    line1 = "Neutral\nHappy\nSad\nSurprise\nAnger"
#                    y0, dy = yy, 35
#                    for ii, txt in enumerate(line1.split('\n')):
#                        y = y0 + ii*dy
#                        cv2.putText(frame_c, txt, (x+55, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#                    i += 1
        
        
        
        
        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        
        ## Drawwwwwwww
        
        
        

        
        # update the background model and increment the total number
        # of frames read thus far
        #md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()
        
def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
# 找找臉在哪裡 (人臉定位): 給予一張照片，回傳人臉座標
def getFaces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor= cascade_scale,
        minNeighbors=cascade_neighbors,
        minSize=minFaceSize,
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    bboxes = []

    for (x,y,w,h) in faces:
        if(w>minFaceSize[0] and h>minFaceSize[1]):
            bboxes.append((x, y, w, h))
    return bboxes

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/emotion_label')
def test():
    global emotion_label
    
    return jsonify(emotion_label)

#####處理path路徑
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)
    
if __name__ == '__main__': 
    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(32,))
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False) 

# release the video stream pointer
vs.stop()