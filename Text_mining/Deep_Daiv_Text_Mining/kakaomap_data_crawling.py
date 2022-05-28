from matplotlib.pyplot import table
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import math

df = pd.DataFrame()

URL = input('크롤링할 웹페이지의 URL을 입력하시오: ')
Kdriver = webdriver.Chrome('Text_mining\chromedriver.exe')
Kdriver.get(URL)

comment_list, temp_comment_list = [], []

class getInfoFromKakao:
    def __init__(self):
        self.comment_list = comment_list
        self.temp_comment_list = temp_comment_list
    
    def Scroll(self):
        body = Kdriver.find_element('css selector', 'body')
        body.send_keys(Keys.END)
        time.sleep(1)
        
    def setComments(self):
        html = Kdriver.page_source
        soup = BeautifulSoup(html, 'lxml')
        children = []
        
        self.temp_comment_list = soup.find_all('p', {'class': "txt_comment"})
        for cmt in self.temp_comment_list:
            children.append(cmt.find('span'))
        self.comment_list.extend(list(map(lambda x : x.text, children)))
        
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
                        next_page = Kdriver.find_element_by_css_selector(f'#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child({idx})')
                        next_page.send_keys(Keys.ENTER)
                    else:
                        break
        return self.comment_list

kakaoINFO = getInfoFromKakao()
kakaoINFO.Scroll()

kakaoHTML = Kdriver.page_source
kakaoSOUP = BeautifulSoup(kakaoHTML, 'lxml')

place_name = kakaoSOUP.find('h2', {'class':'tit_location'}).text
review_count = int(kakaoSOUP.find('strong', {'class':'total_evaluation'}).find('span',{'class':'color_b'}).text)
page_num = math.ceil(review_count/5)

df = df.append(pd.DataFrame(kakaoINFO.gsReviews(page_num), columns=['댓글']))
df.to_csv(f'Text_mining\csv\{place_name}_카카오맵_리뷰_수집.csv')

Kdriver.quit()