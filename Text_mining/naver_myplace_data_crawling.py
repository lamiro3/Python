from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

df = pd.DataFrame()

URL = input("크롤링할 웹페이지의 URL을 입력하시오(네이버 모바일 기준): ")

Ndriver = webdriver.Chrome('Text_mining\chromedriver.exe')
Ndriver.get(URL)

comment_list, visit_count_list = [], []
visits = []

class getInfoFromNaver:
    def __init__(self):
        self.comment_list = comment_list
        self.visit_count_list = visit_count_list
        self.visit_counts = visits

    def plusBtn(self):
        btn = Ndriver.find_element_by_class_name('_3iTUo')
        btn.click()

    def Scroll(self):
        body = Ndriver.find_element('css selector', 'body')
        for rep in range(5):
            body.send_keys(Keys.END)
            time.sleep(1)
            
    def setComments(self, soup):
        self.comment_list = soup.find_all('span', {'class': "WoYOw"})
        self.comment_list = list(map(lambda x : x.text, self.comment_list))
        
    def getComments(self):
        return self.comment_list
    
    def setVSCounts(self, soup): # 방문 횟수 - 클래스명이 같은 태그가 3개가 있어 고민해봐야
        self.visit_count_list = soup.find_all('span', {'class':'_1fvo3'})
        self.visit_count_list = list(map(lambda x : x, self.visit_count_list))
        
    def getVSCounts(self):
        return self.visit_count_list

naverINFO = getInfoFromNaver()
naverHTML = Ndriver.page_source
naverSoup = BeautifulSoup(naverHTML, 'lxml')

review_count = int(naverSoup.find('span', {'class': 'place_section_count'}).text)
place_name = naverSoup.find('span', {'class': '_3XamX'}).text
        
count = 0

while count < review_count:
    naverINFO.Scroll()
    count += 10
    if count < review_count:
        naverINFO.plusBtn()
        print(f'Total {count/review_count*100:.3f}% data collection completed...')
    time.sleep(1)

finalHTML = Ndriver.page_source
finalSoup = BeautifulSoup(finalHTML, 'lxml')

naverINFO.setComments(finalSoup)

df = df.append(pd.DataFrame(naverINFO.getComments(), columns=['댓글']))
df.to_csv(f'Text_mining\csv\{place_name}_네이버_마이플레이스_리뷰_수집.csv')

Ndriver.quit()