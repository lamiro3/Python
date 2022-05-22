import numpy as np
import cv2

#웹캠에서 영상을 읽어온다
cap = cv2.VideoCapture(0)
cap.set(3, 640) #WIDTH
cap.set(4, 480) #HEIGHT

#얼굴 인식 캐스케이드 파일 읽는다
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    #frame = cv2.flip(frame, -1) # 상하반전
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y + h, x:x + w]
    cv2.imshow('video', frame) # video라는 이름으로 출력
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
        break
cap.release()
cv2.destroyAllWindows()
