from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm

def get_images(keyword):
    # 웹 접속 - 네이버 이미지 접속
    print("접속중")
    driver = webdriver.Chrome('C:\\Users\\kr_student2\\Desktop\\automation_edu-master\\automation_edu-master\\image_crawler\\chromedriver')
    driver.implicitly_wait(30)

    url = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query={}'.format(keyword)
    driver.get(url)

    #페이지 스크롤 다운
    body = driver.find_element_by_css_selector('body')
    for i in range(10):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    #이미지 링크 수집
    imgs = driver.find_elements_by_css_selector('img._img')
    result = []
    for img in tqdm(imgs):
        if 'http' in img.get_attribute('src'):
            result.append(img.get_attribute('src'))
    # print(result)

    driver.close()
    print("수집완료")

    #폴더생성
    #print("폴더생성")
    import os
    #if not os.path.isdir('./{}'.format(keyword)):
      #  os.mkdir('./{}'.format(keyword))

    #다운로드
    print("다운로드")
    from urllib.request import urlretrieve
    for index , link in tqdm(enumerate(result)):
        start = link.rfind('.')
        end = link.rfind('&')
        # print(link[start:end])
        filetype = link[start:end] #.png

        urlretrieve(link , 'C:\\Users\\kr_student2\\Desktop\\image\\Toypoodle\\Toypoodle{}{}'.format(index,filetype))


    print("다운로드 완료")

if __name__ == '__main__':
    keyword = input("수집할 이미지 키워드 입력 : ")
    get_images(keyword)