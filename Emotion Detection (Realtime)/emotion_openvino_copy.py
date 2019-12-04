import cv2
import imutils
import time
import operator

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

    # Import 人臉訓練集 Model(找尋人臉定位)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # 宣告基本參數
    cascade_scale = 1.2
    cascade_neighbors = 6
    minFaceSize = (30,30)

    # Specify target device
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)



    # 開啟攝影機
    camera = cv2.VideoCapture(0)
    frameID = 0
    grabbed = True
    start_time = time.time()

    # 攝影無限輪迴
    while grabbed:

        # 讀取攝影機的影像轉成img
        (grabbed, img) = camera.read()
        #img = cv2.resize(img, (286,208))
        img = cv2.resize(img, (550,400))

        # Read an image
        out = []
        frame = img.copy()

        # Call getFaces() 找找臉在哪裡，給予臉部定位
        faces = getFaces(frame)
        x, y, w, h = 0, 0, 0, 0
        i = 0

        for (x,y,w,h) in faces:
            # 臉部的框框
            # cv2.rectangle(影像, 頂點座標, 對向頂點座標, 顏色, 線條寬度)
            cv2.rectangle( frame,(x,y),(x+w,y+h),(0,0,255),2)

            if(w>0 and h>0):
                facearea = frame[y:y+h, x:x+w]

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
                print (max(stats.items(), key=operator.itemgetter(1))[0])

                # 印出來(所有機率、其他文字)
                line2 = "{}%\n{}%\n{}%\n{}%\n{}%".format(neutral,happy,sad,surprise,anger)
                y0, dy = yy, 35
                for ii, txt in enumerate(line2.split('\n')):
                    y = y0 + ii*dy
                    cv2.putText(frame, txt, (x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                line1 = "Neutral\nHappy\nSad\nSurprise\nAnger"
                y0, dy = yy, 35
                for ii, txt in enumerate(line1.split('\n')):
                    y = y0 + ii*dy
                    cv2.putText(frame, txt, (x+55, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                i += 1

        # Save the frame to an image file
        cv2.imshow("FRAME", frame)
        frameID += 1
        fps = frameID / (time.time() - start_time)
        print("FPS:", fps)

        cv2.waitKey(1)