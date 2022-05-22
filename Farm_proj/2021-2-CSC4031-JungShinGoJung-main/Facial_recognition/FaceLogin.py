import cv2
import os
import csv
from PIL import Image, ImageTk
import numpy as np
import pandas as pd

Login_boolean = False
name, Id = '',''
dic = {
    'Name' : name,
    'Ids' : Id
}

def store_data():
    global name, Id, dic
    name = str(input("Enter Name  "))

    Id = str(input("Enter Id   "))

    dic = {
        'Ids': Id,
        'Name': name
    }
    c = dic
    return c


# Fucntion to check if entered ID is number or not
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

# Readface and store data
def TakeImages():
    dict1 = store_data()

    # print(dict1)
    # name = "Santhu"
    # Id = '1'
    if (name.isalpha() and is_number(Id)):
        # Checking Id if it is 1 we are rewriting the profile else just updating csv
        if Id == '1':
            fieldnames = ['Name', 'Ids']
            with open('/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/Profile.csv', 'w') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(dict1)
        else:
            fieldnames = ['Name', 'Ids']
            with open('/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/Profile.csv', 'a+') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                # writer.writeheader()
                writer.writerow(dict1)
        cam = cv2.VideoCapture(0)

        # Haarcascade file for detction of face
        detector = cv2.CascadeClassifier('/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/Cascades/haarcascade_frontalface_default.xml')
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                # Incrementing sample number
                sampleNum = sampleNum + 1
                # Saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/dataset/" + name + "." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                # display the frame
            cv2.imshow('Capturing Face for Login ', img)

            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 60
            elif sampleNum > 50:
                break

        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for Name : " + name + " with ID  " + Id
        print(res)
        print(' [INFO] Exiting Program and cleanup stuff')


    else:
        if (name.isalpha()):
            print('Enter Proper Id')
        elif (is_number(Id)):
            print('Enter Proper name')
        else:
            print('Enter Proper Id and Name')


def getImagesAndLabels(path):
    # Get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    # Create empth face list
    faces = []
    # Create empty ID list
    Ids = []
    # Looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # Loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)

        Ids.append(Id)
    return faces, Ids


# Train image using LBPHFFace recognizer
def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    detector = cv2.CascadeClassifier('/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/Cascades/haarcascade_frontalface_default.xml')
    faces, Id = getImagesAndLabels("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/dataset")
    recognizer.train(faces, np.array(Id))
    # store data in file
    recognizer.save("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/trainer/Trainner.yml")
    res = "Image Trained and data stored in /home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/trainer\TrainData\Trainner.yml "

    print(res)


# This will make sure no duplicates exixts in profile.csv(using Pandas here)



# Fuction to detect the face
def DetectFace():
    df = pd.read_csv('/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/Profile.csv')
    print(df)
    df.sort_values('Ids', inplace=True)
    df.drop_duplicates(subset='Ids', keep='first', inplace=True)
    df.to_csv('/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/Profile.csv', index=False)
    reader = csv.DictReader(open('Profile.csv'))
    print(reader)
    print('Detecting Login Face')
    for rows in reader:
        result = dict(rows)
        print(result)
        if result['Ids'] == '1':
            name1 = result['Name']
        elif result['Ids'] == '2':
            name2 = result["Name"]
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/trainer/Trainner.yml")
    faceCascade = cv2.CascadeClassifier('/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/Cascades/haarcascade_frontalface_default.xml')
    print(faceCascade)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    Face_Id = ''


    # Camera ON Everytime
    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        Face_Id = 'Not detected'

        # Drawing a rectagle around the face
        for (x, y, w, h) in faces:
            Face_Id = 'Not detected'
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            print(Id)
            print(Face_Id)
            print(confidence)

            if (confidence < 90):
                if (Id == 1):
                    name = name1
                    print("for"+name)

                elif (Id == 2):
                    name = name2

                Predicted_name = str(name)
                Face_Id = Predicted_name
                Login_boolean == True
            # else:
            #     Predicted_name = 'Unknown'
            #     Face_Id = Predicted_name
            #     # Here unknown faces detected will be stored
            #     noOfFile = len(os.listdir("UnknownFaces")) + 1
            #     if int(noOfFile) < 100:
            #         cv2.imwrite("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/dataset02/Image" + str(noOfFile) + ".jpg", frame[y:y + h, x:x + w])

            #     else:
            #         pass
            

            # cv2.putText(frame, str(Predicted_name), (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Picture', frame)
        # print(Face_Id)
        cv2.waitKey(1)

        # Checking if the face matches for Login
        if Face_Id == 'Not detected':
            print("-----Face Not Detected, Try again------")
            pass

        elif Face_Id == name1 or name2 :
            print('----------Detected as {}----------'.format(name))
            break

            print('-----------login successfull-------')
            print('***********WELCOME {}**************'.format(name))
            # break
        else:
            print('-----------Login failed please try agian-------')
    cv2.destroyAllWindows()
    return Id 

        # if (cv2.waitKey(1) == ord('q')):
        #   break



# TakeImages()
# TrainImages()
# DetectFace()