import cv2
import imutils
import time
import operator
import threading
from imutils.video import VideoStream

# Import 人臉訓練集 Model(找尋人臉定位)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 宣告基本參數
cascade_scale = 1.2
cascade_neighbors = 6
minFaceSize = (30,30)
print("init")
camera = VideoStream(src=0).start()
time.sleep(2.0)

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

def emotionDetection():
    # Import Trained Model
    model_path = "emotions-recognition-retail-0003.xml"
    pbtxt_path = "emotions-recognition-retail-0003.bin"
    net = cv2.dnn.readNet(model_path, pbtxt_path)
    
    # Specify target device
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

    # 開啟攝影機
    #camera = cv2.VideoCapture(0)
    frameID = 0
    grabbed = True
    start_time = time.time()

    # 攝影無限輪迴
    while grabbed:

        # 讀取攝影機的影像轉成img
        img = camera.read()
        #img = cv2.resize(img, (286,208))
        #img = cv2.resize(img, (550,400))
        img = imutils.resize(img, width=400) 
        # Read an image
        out = []
        frame = img.copy()
        # Save the frame to an image file
        cv2.imshow("FRAME", frame)
        frameID += 1
        fps = frameID / (time.time() - start_time)
        print("FPS:", fps)

        cv2.waitKey(1)

if __name__ == '__main__':
    # start a thread that will perform motion detection
    t = threading.Thread(target=emotionDetection)
    t.daemon = True
    t.start()
    t.join()