from pymysql import NULL
import page_dh
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
import cv2
import FaceLogin
import sys
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import playsound
import os
import pyaudio
import speech_recognition as sr
import time
import simpleaudio
import pygame
from konlpy.tag import Komoran, Kkma, Mecab #3.10 버전 이후에 StreamerLive가 Stream으로 merge 됨
import RPi.GPIO as GPIO
import emotion_faces



class mainWindow(QDialog, page_dh.Ui_Form_main):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
        # self.Pir_run()

    def Pir_run(self):
        t1 = pir_thread(self)
        t1.start()
        


    def OpenLoginClass(self):
        faceid = FaceLogin.DetectFace()
        login_window = login(faceid)
        widget.addWidget(login_window) #####
        widget.setCurrentIndex(widget.currentIndex()+1) ######


class PlaySignal(QObject):
    sig = pyqtSignal()
    def run(self):
        self.sig.emit()


    

class pir_thread( QThread):    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.pirPin = 4
        GPIO.setup(self.pirPin, GPIO.IN, GPIO.PUD_UP)
        
        while True:
            if GPIO.input(self.pirPin) == 1:
                #다음 창 열고, 현재 창 없애는 작업, 초 설정작업 필요
                # print("감지!!!!!!!!!")
                # time.sleep(2)
                # self.OpenLoginClass()
                self.quit()
                break
            else: 
                print( "감지못함") 
        self.OpenLoginClass()
        self.OpenEmotionClass()         
                
    def OpenLoginClass(self):
        self.faceid = FaceLogin.DetectFace()
        login_window = login(self.faceid)
        widget.addWidget(login_window) #####
        widget.setCurrentIndex(widget.currentIndex()+1) ######
    
    def OpenEmotionClass(self):
        emotionClass = emotion(self.faceid)
        widget.addWidget(emotionClass)
        widget.setCurrentIndex(widget.currentIndex()+1)


class login(QDialog, page_dh.Ui_Form_next):
    def __init__(self, faceid):
        super(login, self).__init__()
        self.faceid = faceid
        self.setupUi(self, self.faceid)
        self.playSound()

    def playSound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/asset/medi.mp3")
        time.sleep(1)
        pygame.mixer.music.play()
   


class emotion(QDialog, page_dh.Ui_Form_emotion):
    def __init__(self, faceid):
        super(emotion, self).__init__()
        self.faceid = faceid
        #여기에 위치해 주세요 png
        self.setupUi(self, self.faceid)
        self.playSound()
        self.record()

    def playSound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/asset/mood.mp3")
        pygame.mixer.music.play()
        os.remove("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/asset/mood.mp3")

    def record(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        
        stt = r.recognize_google(audio, language='ko')    
        try: print("Google Speech Recognition thinks you said : " + stt)
        except sr.UnknownValueError: print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e: print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        #텍스트 비식별화
        komoran = Komoran()
        sen = komoran.pos(stt)
        for nlpy in sen:
            if nlpy[1] == 'NNP':
                mk=''
                for a in nlpy[0]:
                    mk = mk + '*'
                print(nlpy[0])
                stt = stt.replace(nlpy[0], mk)
        
        idDate = str(self.faceid) +"_"+time.strftime('%Y_%m_%d', time.localtime(time.time()))
        content = '\n'+idDate +': '+ stt
        file = open('/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/emotion_record/record.txt', 'a') 
        file.write(content)     
        file.close()
        self.capture()
        
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Desktop/mirror/2021-2-CSC4031-JungShinGoJung/Facial_recognition/asset/stretching.mp3")
        pygame.mixer.music.play()
        time.sleep(2)
        self.playVideo(self.faceid)
        self.init()

    def init(self):
        widget.setCurrentIndex(widget.currentIndex()-2)

            









if __name__ == "__main__":
    ###페이스 로그인 아이디 생성
    # FaceLogin.TakeImages()
    # FaceLogin.TrainImages()
    app = QtWidgets.QApplication(sys.argv)
    print("시작")

    ###스택용 위젯
    widget=QtWidgets.QStackedWidget()
    print("시작2")
    ### 다이얼로그 위젯 생성
    main_window = mainWindow()
    widget.addWidget(main_window)

    widget.showFullScreen()
    print("시작3")




    sys.exit(app.exec_())
