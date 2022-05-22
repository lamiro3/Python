import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml");

# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] # dataset dir 밑에 있는 모든 유저들의 이미지 파일 경로를 리스트로 import
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale / convert('1')로 했을 경우에는 점으로 그린 그림마냥 출력됨
        img_numpy = np.array(PIL_img,'uint8') # UPDATE 필요 / uint8 -> ushort / uint8은 더이상 지원하지 않음.
        id = int(os.path.split(imagePath)[-1].split(".")[1]) # face_dataset에서 부여한 번호를 각 이미지의 id로 전환
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
