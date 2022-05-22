import numpy as np
import cv2 as cv
from keras.models import load_model
import time


# happy, neutral return 1, others return 0

def convert_dtype(x):
    x_float = x.astype('float32')
    return x_float


def normalize(x):
    x_n = (x - 0) / (255)
    return x_n


def reshape(x):
    x_r = x.reshape((x.shape[0], x.shape[1], x.shape[2], 1))
    return x_r



def emotion(faceid):
    model = load_model('Emotion_recognition/first_5322_model.hdf5')
    face_cascade = cv.CascadeClassifier('Emotion_recognition/haarcascade_frontalface_default.xml')
    cam = cv.VideoCapture(0)
    filename = str(faceid) +"_"+time.strftime('%Y_%m_%d', time.localtime(time.time()))+".jpg"
    n =0
    emotion_result = []
    while True :
        img = cam.read()[1]
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            roi_gray = cv.resize(roi_gray, (48, 48), interpolation=cv.INTER_AREA)
            roi_gray = convert_dtype(np.array([roi_gray]))
            roi_gray = normalize(roi_gray)
            roi_gray = reshape(roi_gray)
            pr = model.predict(roi_gray)[0]
            
            max_emo = np.argmax(pr)
            
            if (max_emo == 2 or max_emo == 5):
                result = 1
            else:
                result = 0
            emotion_result.append(result)
            n = n+1
            print('n :'+str(n))
            
            if n == 11 :
                break
        if n == 11:
            eyeCascade = cv.CascadeClassifier('Facial_recognition/Cascades/haarcascade_eye.xml')
            for (x, y, w, h) in faces:
                # cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # 눈 찾기
                roi_color = img[y:y + h, x:x + w]
                roi_gray = gray[y:y + h, x:x + w]
                eyes = eyeCascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), -1)
                    roi = roi_color[ey:ey+eh, ex:ex+ew]
                    roi = cv.blur(roi, (30, 30))
                    img[ey:ey+eh, ex:ex+ew] = roi
            cv.imwrite("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/emotion_capture/"+filename,img)
            cv.destroyAllWindows()
            break
        
        cv.imshow('img', img)
        keypress = cv.waitKey(1)
        if keypress == ord('q'):
            cv.destroyAllWindows()
            break
    print(emotion_result)
    emotion_result.sort()
    print(emotion_result)
    print(emotion_result[5])
    return emotion_result[5]
# print(emotion(1))
