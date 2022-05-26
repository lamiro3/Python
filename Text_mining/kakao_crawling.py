from matplotlib.pyplot import table
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import math
from selenium.common.exceptions import NoSuchElementException
import warnings
warnings.filterwarnings('ignore')
import numpy as np

df = pd.DataFrame()

URL = input('크롤링할 웹페이지의 URL을 입력하시오: ')
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
Kdriver = webdriver.Chrome('chromedriver.exe',options=options)
Kdriver.get(URL)

comment_list, temp_comment_list, rates_list = [], [], []
columns = ['score', 'review']
review_df = pd.DataFrame(columns=columns)

class getInfoFromKakao:
    def __init__(self):
        self.comment_list = comment_list
        self.temp_comment_list = temp_comment_list
        self.rates_list = rates_list
        self.columns = columns
        self.review_df = review_df
    
    def Scroll(self):
        body = Kdriver.find_element('css selector', 'body')
        body.send_keys(Keys.END)
        time.sleep(1)
        
    def setComments(self):
        html = Kdriver.page_source
        soup = BeautifulSoup(html, 'lxml')
        children = []

        contents_div = soup.find(name="div", attrs={"class":"evaluation_review"})
        self.temp_comment_list = contents_div.find_all('p', {'class': "txt_comment"})
        self.rates_list = contents_div.find_all("em", {"class":"num_rate"})
        for rate, review in zip(self.rates_list, self.temp_comment_list):
            if review != ' ':
                row = [rate.text[0], review.find(name="span").text]
                series = pd.Series(row, index=columns)
                self.review_df = self.review_df.append(series, ignore_index=True)
        
    def is_5_or_6(self):
        if Kdriver.find_element_by_class_name('cont_visitor'):
            return 6
        else:
            return 5
    
    def gsReviews(self, pn):  
        
        tab_num = math.ceil(pn/5)
        
        for _ in range(tab_num):
            for i in range(1, 6):
                self.Scroll()
                self.setComments()
                idx = 0
            
                if (i+5*_)&5 == 1 and (i+5*_)%5 == 2:
                    idx = 3 if _ == 0 else 4
                elif (i+5*_)%5 == 0:
                    idx = 6 if _ == 0 else 7
                else :
                    idx = (i+5*_)%5+2 if _ == 0 else (i+5*_)%5+3
                    
                tab_idx = 5 if _ == 0 else 6
                
                if _ == tab_num-1 and _ != 0:
                    if pn%5 != 0:
                        if (i+5*_)&5 == 0:
                            idx = 4
                        elif (i+5*_)&5 == 1:
                            idx = 5
                        elif (i+5*_)&5 == 2:
                            idx = 6
                        elif (i+5*_)&5 == 3:
                            idx = 7
                        else:
                            idx = 8

                print(f'Total {(i+5*_)/pn*100:.3f}% data collection completed...')
            
                if (i+5*_)%5 == 0 and (i+5*_) < pn:
                    next_tab = Kdriver.find_element_by_xpath(f'//*[@id="mArticle"]/div[{self.is_5_or_6()}]/div[3]/div/a[{tab_idx}]')
                    next_tab.send_keys(Keys.ENTER)
                
                else:
                    if (i+5*_) < pn:
                        try:
                            next_page = Kdriver.find_element_by_css_selector(f'#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child({idx})')
                            next_page.send_keys(Keys.ENTER)
                        except NoSuchElementException:
                            print("NoSuchElementException")
                    else:
                        break
        return self.review_df

kakaoINFO = getInfoFromKakao()
kakaoINFO.Scroll()

kakaoHTML = Kdriver.page_source
kakaoSOUP = BeautifulSoup(kakaoHTML, 'lxml')

place_name = kakaoSOUP.find('h2', {'class':'tit_location'}).text
review_count = int(kakaoSOUP.find('strong', {'class':'total_evaluation'}).find('span',{'class':'color_b'}).text)
page_num = math.ceil(review_count/5)

df = kakaoINFO.gsReviews(page_num)
df['review'].replace('', np.nan, inplace=True)
df.dropna(subset=['review'], inplace=True)
df.to_csv(f'{place_name}_kakao_review.csv',encoding='utf-8',index=False)

Kdriver.quit()
