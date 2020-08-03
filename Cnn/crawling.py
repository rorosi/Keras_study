from selenium import webdriver
import requests as req
import time
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
import os


# 찾고자 하는 검색어를 url로 만들어 준다.
searchterm = '말티즈강아지'
# 경로 + 검색어
url = "https://search.naver.com/search.naver?where=image&section=image&query=" + searchterm
#크롬 창을 백그라운드로 돌리면 이미지를 중복해서 다운받음
#options를 통해 크롬창을 숨기고 백그라운드에서도 실행될 수 있게 설정
options = webdriver.ChromeOptions()
options.add_argument('headless') #Headless 옵션. 모두 완성한 뒤 백그라운드로 돌릴 경우에
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu") #headless 모드일 경우 gpu 끄기
# 혹은 options.add_argument("--disable-gpu")

# 브라우저를 크롬으로 만들어주고 인스턴스를 생성해준다.
browser = webdriver.Chrome('C:\\Users\\kr_student2\\Desktop\\automation_edu-master\\automation_edu-master\\image_crawler\\chromedriver', options=options)
# 브라우저를 오픈할 때 시간간격을 준다.
browser.implicitly_wait(3)
# 해당 경로로 브라우져를 오픈해준다.


browser.get(url)
time.sleep(1)

for _ in range(10000):
    # 가로 = 0, 세로 = 30000 픽셀 스크롤한다.
    browser.execute_script("window.scrollBy(0,30000)")

count = 0
photo_list = []

# span태그의 img_border클래스를 가져옴
photo_list = browser.find_elements_by_tag_name("span.img_border")

# 소스코드가 있는 경로에 '검색어' 폴더가 없으면 만들어준다.(이미지 저장 폴더를 위해서)
#if not os.path.exists('Maltese'):
 #   os.mkdir('C:\\Users\\kr_student2\\Desktop\\image\\Maltese')

for index, img in enumerate(photo_list[0:]):
    # 위의 큰 이미지를 구하기 위해 위의 태그의 리스트를 하나씩 클릭한다.
    img.click()

    # 확대된 이미지의 정보는 img태그의 _image_source라는 class안에 담겨있다.
    html_objects = browser.find_element_by_tag_name('img._image_source')
    current_src = html_objects.get_attribute('src')

    t = urlopen(current_src).read()
    if index < 50:  # 40
        filename = 'Maltese' + str(count) + ".jpg"
        File = open(os.path.join('C:\\Users\\kr_student2\\Desktop\\image\\Maltese', 'Maltese' + str(count) + ".jpg"), "wb")
        File.write(t)
        count += 1
        # before_src = current_src 조금 더 고민
        # current_src = ""
        print("img save" + str(count))
    else:
        print("저장 성공")
        browser.close()
        break
