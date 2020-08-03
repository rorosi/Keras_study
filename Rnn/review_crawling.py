from bs4 import BeautifulSoup

from selenium import webdriver

import time

import sys

import re

import math

import numpy

import pandas as pd

import xlwt

import random

import os

from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_argument('headless') #Headless 옵션. 모두 완성한 뒤 백그라운드로 돌릴 경우에
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu") #headless 모드일 경우 gpu 끄기

query_txt = input("\n\n\t1. 크롤링할 영화의 제목을 입력하세요: ")

cnt = int(input("\t2. 크롤링할 건수는 몇 건입니까?: "))

page_cnt = math.ceil(cnt / 10)

f_dir = input("\t3. 결과파일을 저장할 폴더주소만 쓰세요.(예 : C:\pytest\): ")

print("\n\n크롤링할 총 페이지 번호 :  %d" % page_cnt)

print("=" * 80)

n = time.localtime()

s = '%04d-%02d-%02d-%02d-%02d-%02d' % (n.tm_year, n.tm_mon, n.tm_mday, n.tm_hour, n.tm_min, n.tm_sec) #현재 시간

os.makedirs(f_dir + s + '-' + query_txt)

os.chdir(f_dir + s + '-' + query_txt)

ff_name = f_dir + s + '-' + query_txt + '\\' + s + '-' + query_txt + '.txt'

fc_name = f_dir + s + '-' + query_txt + '\\' + s + '-' + query_txt + '.csv'

fx_name = f_dir + s + '-' + query_txt + '\\' + s + '-' + query_txt + '.xls'

s_time = time.time()

path = 'C:\\Users\\kr_student2\\Desktop\\automation_edu-master\\automation_edu-master\\image_crawler\\chromedriver'

driver = webdriver.Chrome(path, options=options)

driver.get('https://movie.naver.com/')

time.sleep(2)

driver.find_element_by_xpath('''//*[@id="ipt_tx_srch"]''').click()

element = driver.find_element_by_xpath('''//*[@id="ipt_tx_srch"]''')

element.send_keys(query_txt)

driver.find_element_by_xpath('''//*[@id="jSearchArea"]/div/button''').click()

driver.find_element_by_xpath("""//*[@id="old_content"]/ul[2]/li[1]/dl/dt/a""").click()

driver.find_element_by_xpath("""//*[@id="movieEndTabMenu"]/li[5]/a""").click()

driver.switch_to.frame("pointAfterListIframe")

number = [] # 번호 컬럼
contents = []  # 리뷰 내용 컬럼

k = 11

p = 1

for x in range(1, page_cnt + 1):

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    content = soup.select('''body > div > div > div.score_result > ul > li div.score_reple > p''')

    if x == page_cnt: #페이지 번호
        k = cnt % 10 + 1

    for i in range(1, k):
        f = open(ff_name, 'a', encoding="UTF-8")

        content1 = content[i - 1].get_text().strip()

        print("총 %d 건 중 %d 번째 리뷰 데이터를 수집합니다." % (cnt, (x - 1) * 10 + i) + "=" * 30)

        f.write("총 %d 건 중 %d 번째 리뷰 데이터를 수집합니다." % (cnt, (x - 1) * 10 + i) + "=" * 30 + "\n")

        print("2. 리뷰내용 : %s" % content1)

        f.write("2. 리뷰내용 : %s" % content1 + "\n")

        contents.append(content1)
        number.append((x - 1) * 10 + i)

        f.write("\n")

        print("\n")

        f.close()

        print("\n")

    if (p % 10 == 0):

        driver.find_element_by_xpath('''//*[@id="pagerTagAnchor2"]/em''').click()

    else:

        driver.find_element_by_link_text("""%s""" % (x + 1)).click()  # 다음 페이지번호 클릭

    time.sleep(2)

    p += 1

result = pd.DataFrame()
result['번호'] = number
result['리뷰내용'] = contents


# csv 형태로 저장하기

result.to_csv(fc_name, encoding="utf-8-sig", index=True)

# 엑셀 형태로 저장하기

result.to_excel(fx_name, index=True)

e_time = time.time()  # 검색이 종료된 시점의 timestamp 를 지정합니다

t_time = e_time - s_time

print("\n")

print("=" * 80)

print("총 소요시간은 %s 초 입니다 " % round(t_time, 1))

print("파일 저장 완료: txt 파일명 : %s " % ff_name)

print("파일 저장 완료: csv 파일명 : %s " % fc_name)

print("파일 저장 완료: xls 파일명 : %s " % fx_name)

print("=" * 80)

driver.close()